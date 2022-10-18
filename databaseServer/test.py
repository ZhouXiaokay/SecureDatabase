import pymysql
from pymysql import converters
import tenseal as ts
pk_file = "../transmission/ts_ckks.config"
pk_bytes = open(pk_file, "rb").read()
pk_ctx = ts.context_from(pk_bytes)

db = pymysql.connect(host='localhost',
                     user='root',
                     password='199966',
                     database='database_{0}'.format(1))

sql = "SELECT SUM({0}),COUNT({0}) FROM {1}".format("VALUE1", "DATA_A")

cursor = db.cursor()
cursor.execute(sql)
results = cursor.fetchone()
# close conn
db.close()
print(results[0],results[1])

l=[]
for i in range(len(results)):

    l.append(results[i])
print(l)
plain_vector = ts.plain_tensor(l)
print(plain_vector)
enc_vector = ts.ckks_vector(pk_ctx, plain_vector)
enc_1 = enc_vector**(-1)
lis=[]
lis.append(enc_vector)
lis.append(enc_vector)
print(enc_1.decrypt())
