
var jwt = require('jwt-simple')
var { logger } = require('../util/mylogger')
const myMiddleWare = {
  verifyToken: (req, res, next) => {
    // the myMiddleWare always run twice out of no reason, one of these not taking my data, so i omiss one of these.
    if (req.get('access-control-request-method') == null) {
      logger.info('[Access]:[path %s]【IP%s】',req.originalUrl,req.ip)
      if (req.originalUrl != '/user/gettoken') {
        var token = req.get('token')
        let tokenContainedInfo
        try {
          tokenContainedInfo = jwt.decode(token, 'secrettt')
        }
        catch (e) {
          logger.info('token wrong!')
          return res.sendStatus(401)
        }
        req.tokenContainedInfo = tokenContainedInfo
      }
    }
    next()
  },
  header: (req, res, next) => {
    res.header("Access-Control-Allow-Origin", '*');
    res.header("Access-Control-Allow-Headers", "token,content-type,productId,X-Requested-With");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By", ' 3.2.1')
    res.header("Content-Type", "application/json;charset=utf-8");
    next();
  }
}
module.exports = {
  myMiddleWare,
}