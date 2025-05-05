from peewee import Model, PostgresqlDatabase, CharField, DateTimeField, IntegerField, FloatField, BlobField
# Configuración de la base de datos
db_config = {
    'host': 'localhost', 
    'port': 5432, 
    'user': 'postgres', 
    'password': 'postgres', 
    'database': 'db'
}
db = PostgresqlDatabase(**db_config)

# Definición de un modelo
class BaseModel(Model):
    class Meta:
        database = db

# Ahora puedes definir tus modelos específicos heredando de BaseModel
# y db estará conectado al servicio de PostgreSQL cuando realices operaciones de base de datos.


## Ver la documentación de peewee para más información, es super parecido a Django

class Datos(BaseModel):
    # Dispositivo
    device_id = CharField()
    device_mac = CharField()
    
    ##  Data  ##
    batt_level = IntegerField()
    timestamp = DateTimeField()
    # THPC_Sensor
    temp = IntegerField(null=True)
    press = IntegerField(null=True)
    hum = IntegerField(null=True)
    co = FloatField(null=True)
    # Acceloremeter_kpi
    rms = FloatField(null=True)
    amp_x = FloatField(null=True)
    frec_x = FloatField(null=True)
    amp_y = FloatField(null=True)
    frec_y = FloatField(null=True)
    amp_z = FloatField(null=True)
    frec_z = FloatField(null=True)
    # Acceloremeter_Sensor
    acc_x = BlobField(null=True)
    acc_y = BlobField(null=True)
    acc_z = BlobField(null=True)
    rgyr_x = BlobField(null=True)
    rgyr_y = BlobField(null=True)
    rgyr_z = BlobField(null=True)

class Logs(BaseModel):
    device_id = CharField()
    transport_layer = IntegerField()
    protocol_id = IntegerField()
    timestamp = DateTimeField()

class Configuracion(BaseModel):
    protocol_id = IntegerField()
    transport_layer = IntegerField()

class Loss(BaseModel):
    delay = FloatField()
    packet_loss = FloatField()


# Creacion de tablas como script
def create_tables():
    with db:
        db.create_tables([Datos, Logs, Configuracion, Loss])
        print("Tablas creadas exitosamente.")

if __name__ == "__main__":
    # Conectar y crear
    db.connect()
    create_tables()