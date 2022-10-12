import tenseal as ts
import torch
sk_file = "ts_ckks.config"
pk_file = "ts_ckks_pk.config"

pk_bytes = open(pk_file, "rb").read()
pk_ctx = ts.context_from(pk_bytes)

sk_bytes = open(sk_file, "rb").read()
sk_ctx = ts.context_from(sk_bytes)
sk = sk_ctx.secret_key()


plain_vector = ts.plain_tensor([60,50])
enc_1 = ts.ckks_vector(pk_ctx,plain_vector)
enc_2 = ts.ckks_vector(sk_ctx,plain_vector)

print(enc_2.decrypt())
print(enc_1.decrypt(sk))
