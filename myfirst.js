
const Client = require('ssh2').Client;

// Create a new SSH client instance
const sshClient = new Client();

// Configure the connection parameters
const connectionParams = {
  host: 'raspberrypi',
  username: 'class380',
  password: 'project'
  //privateKey: require('fs').readFileSync('/path/to/your/private-key')
};

// Connect to the SSH server
sshClient.connect(connectionParams);


// Handle events when the connection is established

sshClient.on('ready', () => {
    console.log('Connected via SSH!');
    //execute();

// Now you can execute commands, transfer files, etc.

});

// Handle errors during the SSH connection process

sshClient.on('error', (err) => {
    console.error('Error connecting via SSH:', err);

});

/*
function execute() {
  // Prompt the user to enter a command
  rl.question('Enter a command to execute on the remote server: ', (command) => {
    // Execute the user-entered command on the remote server
    sshClient.exec(command, (err, stream) => {
      if (err) throw err;

      stream
        .on('close', (code, signal) => {
          console.log('Command execution closed');
          sshClient.end();
          rl.close();
        })
        .on('data', (data) => {
          console.log('Command output:', data.toString());
        })
        .stderr.on('data', (data) => {
          console.error('Command error:', data.toString());
        });
    });
  });
}
*/



