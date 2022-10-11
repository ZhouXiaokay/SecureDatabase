import tenseal as ts

sk_file = "ts_ckks.config"
pk_file = "ts_ckks_pk.config"

pk_bytes = open(pk_file, "rb").read()
pk_ctx = ts.context_from(pk_bytes)

sk_bytes = open(sk_file, "rb").read()
sk_ctx = ts.context_from(sk_bytes)
sk = sk_ctx.secret_key()


plain_vector = ts.plain_tensor([60])
enc = ts.ckks_vector(pk_ctx,plain_vector)
print(enc.decrypt(sk))