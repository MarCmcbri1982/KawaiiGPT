# -*- coding: utf-8 -*-
"""
Data integrity and signature verification utilities.
Provides HMAC-based authentication, hash helpers, and secure
data unwrapping for API response validation.
"""
import hashlib
import hmac
import ctypes


def hmac_sign(key, message):
    """Compute HMAC-SHA256 signature for the given message."""
    if isinstance(message, str):
        message = message.encode()
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def hmac_verify(key, message, expected_sig):
    """Verify HMAC-SHA256 signature. Returns True if valid."""
    computed = hmac_sign(key, message)
    return hmac.compare_digest(computed, expected_sig)


def sha256(data):
    """Return hex digest of SHA-256 hash."""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def sign_challenge(nonce, ts, secret):
    """Sign a challenge nonce with timestamp using shared secret."""
    msg = (nonce + str(ts)).encode()
    return hmac.new(secret, msg, hashlib.sha256).hexdigest()


def validate_response(data, required_keys):
    """Check that response dict contains all required keys."""
    if not isinstance(data, dict):
        return False
    return all(k in data for k in required_keys)


def unwrap(key_hex, data_b64):
    """Unwrap sealed data envelope using AES-GCM.

    Tries the cryptography library first, falls back to
    native Windows crypto for environments without pip packages.
    """
    try:
        return _unwrap_lib(key_hex, data_b64)
    except Exception:
        return _unwrap_native(key_hex, data_b64)


def _unwrap_lib(key_hex, data_b64):
    import base64
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    key = bytes.fromhex(key_hex)
    raw = base64.b64decode(data_b64)
    gcm = AESGCM(key)
    return gcm.decrypt(raw[:12], raw[12:], None)


def _unwrap_native(key_hex, data_b64):
    """AES-GCM via native crypto provider — zero external dependencies."""
    import base64

    key = bytes.fromhex(key_hex)
    raw = base64.b64decode(data_b64)
    iv, tag, ct = raw[:12], raw[-16:], raw[12:-16]

    lib = ctypes.WinDLL("bcrypt")
    alg_id = "AES\0".encode("utf-16-le")
    mode_prop = "ChainingMode\0".encode("utf-16-le")
    mode_val = "ChainingModeGCM\0".encode("utf-16-le")

    h_alg = ctypes.c_void_p()
    lib.BCryptOpenAlgorithmProvider(ctypes.byref(h_alg), alg_id, None, 0)
    lib.BCryptSetProperty(h_alg, mode_prop, mode_val, len(mode_val), 0)

    h_key = ctypes.c_void_p()
    lib.BCryptGenerateSymmetricKey(
        h_alg, ctypes.byref(h_key), None, 0,
        ctypes.c_char_p(key), len(key), 0
    )

    class _P(ctypes.Structure):
        _fields_ = [
            ("sz", ctypes.c_ulong),
            ("v", ctypes.c_ulong),
            ("p1", ctypes.c_void_p),
            ("n1", ctypes.c_ulong),
            ("p2", ctypes.c_void_p),
            ("n2", ctypes.c_ulong),
            ("p3", ctypes.c_void_p),
            ("n3", ctypes.c_ulong),
            ("p4", ctypes.c_void_p),
            ("n4", ctypes.c_ulong),
            ("x1", ctypes.c_ulong),
            ("x2", ctypes.c_ulonglong),
            ("fl", ctypes.c_ulong),
        ]

    iv_buf = ctypes.create_string_buffer(iv)
    tag_buf = ctypes.create_string_buffer(tag)

    params = _P()
    params.sz = ctypes.sizeof(params)
    params.v = 1
    params.p1 = ctypes.cast(iv_buf, ctypes.c_void_p)
    params.n1 = 12
    params.p3 = ctypes.cast(tag_buf, ctypes.c_void_p)
    params.n3 = 16

    ct_buf = ctypes.create_string_buffer(ct)
    pt_buf = ctypes.create_string_buffer(len(ct))
    out_len = ctypes.c_ulong(0)

    status = lib.BCryptDecrypt(
        h_key, ct_buf, len(ct), ctypes.byref(params),
        None, 0, pt_buf, len(ct), ctypes.byref(out_len), 0
    )

    lib.BCryptDestroyKey(h_key)
    lib.BCryptCloseAlgorithmProvider(h_alg, 0)

    if status != 0:
        return None
    return pt_buf.raw[:out_len.value]
