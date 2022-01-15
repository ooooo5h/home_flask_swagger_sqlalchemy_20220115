from server import create_app

app = create_app('ProductionConfig')
app.run(host='0.0.0.0')