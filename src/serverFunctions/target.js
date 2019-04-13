var { sdao } = require('../util/dao')
var { logger } = require('../util/mylogger')
var fs = require('fs')
const uploadDir = './uploadTargets/'
const target = {

  uploadDir,
add: async (req, res) => {
    var file = req.file
    try {
      fs.renameSync(uploadDir + file.filename, uploadDir + file.originalname)
    }
    catch (e) {
      console.log(e)
      return res.sendStatus(501)
    }
    var lines = []
    try {
      var read = fs.readFileSync(uploadDir + file.originalname, 'utf-8')
      fs.closeSync()


    }
    catch (e) {
      console.log(e)
      return res.sendStatus(501)
    }
    lines = read.split('\n')
    var ipRange=[]
    for (var line of lines) {
      // var myregE=new RegExp('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$')
      if (line == '') continue
      ipRange.push(line)

    }
    var newTarget = {
      name: file.originalname,
      createdby: req.tokenContainedInfo.user,
      description: '',
      lines: ipRange.length,
      ipRange,

      uploadAt: Date.now(),
    }
    await sdao.insert('target', newTarget)
    res.json('ok')
  },
  delete: async (req, res) => {
    var id = req.body.targetId
    if (id == null)
      return res.sendStatus(415)
    sdao.delete('target', { _id: id })
    res.json('ok')
  },
  update: async (req, res) => {
    console.log(req.body)
    var id = req.body.targetId
    var update = req.body.update
    if (id == null || update == null)
      return res.sendStatus(415)
    await sdao.update('target', { _id: id }, update)
    res.json('ok')
  },
  get: async (req, res) => {
    var condition = req.body.condition
    if (condition == null)
      condition = {}
    let result = await sdao.findField('target', condition)
    for (var record of result) {
      delete record.ipRange
    }
    res.json(result)
  },
  getZmapResult: async (req, res) => {
    // var condition = req.body.condition
    // if (condition == null)
    // condition = {}
    // let result=await sdao.findField('zmapResults', {complete:true},{results:-1})
    // for(var r of result)
    // delete r.results
    // res.json(result)
    var condition = req.body.condition
    if (condition == null)
      condition = {}
    let result = await sdao.find('target', condition)
    res.json(result)
  }
}
module.exports = {
  target,
}