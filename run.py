from project import app, socketio

# app.run(debug = True)
socketio.run(app, host="0.0.0.0")
