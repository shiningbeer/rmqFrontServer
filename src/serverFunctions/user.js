var { sdao } = require('../util/dao')
var { logger } = require('../util/mylogger')
var jwt = require('jwt-simple')
const user = {
  add: async (req, res) => {
    var newUser = req.body.newUser
    if (newUser == null)
      return res.sendStatus(415)
    let newUserToAdd = {
      ...newUser,
      taskCount: 0,
      lastLoginAt: Date.now(),
      lastLoginIp: '21.34.56.78'
    }
    //todo: verify validity of newUser
    await sdao.insert('user', newUserToAdd)
    res.json('ok')
  },
  delete: async (req, res) => {
    var id = req.body.userId
    if (id == null)
      return res.sendStatus(415)
    await sdao.delete('user', { _id: id })
    res.json('ok')
  },
  modpw: async (req, res) => {
    var id = req.body.userId
    var pw = req.body.pw
    if (id == null || pw == null)
      return res.sendStatus(415)
    await sdao.update('user', { _id: id }, { password: pw })
    res.json('ok')
  },
  getToken: async (req, res) => {
    console.log(req.body)
    var user = req.body.userName
    var pw = req.body.password
    var type=req.body.type
    if (user == null || pw == null)
      return res.sendStatus(415)
    let result = await sdao.find('user', { name: user, password: pw })
    console.log(result)
    if (result.length < 1)
      res.json({status:'no'})
    else {
      let userInfo = result[0]
      let token = jwt.encode({ user: userInfo.name, type: userInfo.authority }, 'secrettt')
      res.json({
        status: 'ok',
        type,
        currentAuthority: userInfo.authority,
        currentUser:userInfo.name,
          token,
      })
    }
  },
  get: async (req, res) => {
    var condition = req.body.condition
    if (condition == null)
      condition = {}
    let result=await sdao.find('user', condition)
    res.json(result)
  },
}
module.exports = {
  user,
}