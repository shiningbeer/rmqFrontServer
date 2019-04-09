var { sdao } = require('../util/dao')
var fs = require('fs')
var { logger } = require('../util/mylogger')
const uploadDir = './uploadPlugins/'
const plugin = {
  uploadDir,
  add: async (req, res) => {
    var file = req.file
    try {
      fs.renameSync(uploadDir + file.filename, uploadDir + file.originalname)
    }
    catch (e) {
      return res.sendStatus(501)
    }
    var newplugin = {
      name: file.originalname,
      user: 'lele',
      description: '',
      protocal: '',
      usedCount: 0,
      port: '',
      uploadAt: Date.now(),
    }
    await sdao.insert('plugin', newplugin)
    res.json('ok')
  },
  delete: async (req, res) => {
    var pluginName = req.body.pluginName
    if (pluginName == null)
      return res.sendStatus(415)

    var err = await new Promise((resolve, reject) => {
      fs.unlink(uploadDir + '/' + pluginName, (err) => {
        resolve(err)
      })
    })
    if (err)
      return res.sendStatus(500)
    await sdao.delete('plugin', { name: pluginName })
    res.json('ok')

  },
  update: async (req, res) => {
    const { name, update } = req.body
    if (name == null || update == null)
      return res.sendStatus(415)
    await sdao.update('plugin', { name }, update)
    res.json('ok')
  },
  get: async (req, res) => {
    let plugins
    try {
      plugins = fs.readdirSync(uploadDir)
    }
    catch (e) {
      return res.sendStatus(500)
    }

    let result = []
    for (var item of plugins) {
        let oneplugin=await sdao.findone('plugin', { name: item })
      if (oneplugin != null)
        result.push(oneplugin)
    }
    // console.log(result)
    res.json(result)
  },
}
module.exports = {
  plugin
}