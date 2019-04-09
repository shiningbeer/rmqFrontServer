var { sdao } = require('../util/dao')
var { logger } = require('../util/mylogger')
var fs = require('fs')
const uploadDir = './uploadTargets/'
const targetI = {
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


    }
    catch (e) {
      console.log(e)
      return res.sendStatus(501)
    }
    lines = read.split('\n')
    var ipRange=[]
    for (var line of lines) {
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
    await sdao.insert('targetI', newTarget)
    res.json('ok')
  },
  delete: async (req, res) => {
    var id = req.body.targetId
    if (id == null)
      return res.sendStatus(415)
    sdao.delete('targetI', { _id: id })
    res.json('ok')
  },
  update: async (req, res) => {
    console.log(req.body)
    var id = req.body.targetId
    var update = req.body.update
    if (id == null || update == null)
      return res.sendStatus(415)
    await sdao.update('targetI', { _id: id }, update)
    res.json('ok')
  },
  get: async (req, res) => {
    var condition = req.body.condition
    if (condition == null)
      condition = {}
    let result = await sdao.findField('targetI', condition)
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
    let result = await sdao.find('targetI', condition)
    res.json(result)
  }
}
module.exports = {
  targetI,
}