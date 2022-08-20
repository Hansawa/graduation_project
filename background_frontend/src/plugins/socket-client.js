import io from 'socket.io-client'

export function getSocketIO() {
    // namespace:命名空间或path
    const url = 'http://127.0.0.1:8080'
    const options = {
        path: '',
        transports: ['websocket'],
        reconnectionAttempts: 3,
        reconnectionDelay: 3000,
        timestampRequests: true,
        autoConnect: false
    }
    const socket = io(url, options)
    return socket
}
