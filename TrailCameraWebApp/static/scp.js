
const { Client } = require('node-scp')

Client({
  host: 'raspberrypi',
  port: 22,
  username: 'class380',
  password: 'project',
  // privateKey: fs.readFileSync('./key.pem'),
  // passphrase: 'your key passphrase',
}).then(client => {
  client.downloadDir(
    '/home/class380/Desktop/dataFinal',
    './images',
    // options?: TransferOptions
  )
  .then(response => {
    client.emptyDir('/home/class380/Desktop/dataFinal')
      .then(() =>{
        client.close() // remember to close connection after you finish
      })
  })
  .catch(error => console.log(error))
}).catch(e => console.log(e))

