import tenseal as ts

context = ts.context(ts.SCHEME_TYPE.BFV, poly_modulus_degree=4096, plain_modulus=1032193)

sk = context.secret_key()

context.make_context_public()

plain_vector = [60]
encrypted_vector = ts.bfv_vector(context, plain_vector)

plain2_vector = [1]
encrypted2_vector = ts.bfv_vector(context, plain2_vector)

