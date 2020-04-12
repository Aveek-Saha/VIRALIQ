import eventlet
import socketio

from retrieve_videos import searchVid

sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def search(sid, data):
    print('message ', data)
    vr = searchVid(data['input'])

    ranks = []
    for i in sorted(vr):
        ranks.append((i, vr[i]))

    ranks.sort(key=lambda x: x[1], reverse=True)
    # print('ranks', ",".join([x + ":" + str(y) for (x, y) in ranks][:5]))
    sio.emit('ranks', {'output': ranks[:5]})



@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 8080)), app)
