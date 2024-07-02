const net = require('net');

const serverAddress = './tmp/socket_file';
console.log(`connecting to ${serverAddress}`);

const requestData = {
    method: "nroot",
    params: [2, 4],
    param_types: ["int", "int"],
    id: 1
};

const jsonRequestData = JSON.stringify(requestData);

const client = net.createConnection({ path: serverAddress }, () => {
    console.log(`connected to ${serverAddress}`);
    client.write(jsonRequestData);
});

client.on('error', (err) => {
    console.error('Connection error:', err);
    process.exit(1);
});

client.on('data', (data) => {
    console.log('Server response:' + data.toString());
});

client.setTimeout(2000, () => {
    console.log('Socket timeout, ending listening for server messages');
    client.end();
});

client.on('end', () => {
    console.log('disconnected from server');
});

client.on('close', () => {
    console.log('closing socket');
});