var { adao, sdao } = require('./util/dao')
var { logger } = require('./util/mylogger')
const { sdao: sdao_cidr } = require('./util/dao_cidr')
const { sdao: sdao_ipv4 } = require('./util/dao_ipv4')

adao.connect("mongodb://localhost:27017", 'cent', async (err) => {
    err ? logger.info('db connection fail!') : logger.info('task runner starts!')

    await sdao_cidr.connect("mongodb://localhost:27017", 'cidrTask')
    await sdao_ipv4.connect("mongodb://localhost:27017", 'ipv4Task')
    //when the program starts, reset all the tasks the realTaskCreating as false
    await sdao.update('task', {}, { realTaskCreating: false })
    //dealing with the task just started and the realTask not created
    setInterval(async () => {
        var startTasks = await sdao.find('task', { realTaskCreated: false, realTaskCreating: false })
        for (var task of startTasks) {
            const { _id: taskId, type, stage,port,selectedTargets,paused} = task
            //first to mark the task is udergoing creating real task
            await sdao.update('task', { _id: taskId }, { realTaskCreating: true })

            if (type == 'plugin') {
                //take out all the targets and create the progress table
                var totoalcount = 0
                for (var target of selectedTargets) {
                    var re = await sdao.findone('targetI', { _id: target._id })
                    var lines_no = 0
                    for (var item of re.ipRange) {
                        lines_no = lines_no + 1
                        var doc = { ip: item, port }
                        await sdao_ipv4.insert(taskId.toString(), doc)
                    }
                    totoalcount = totoalcount + lines_no

                }
                //after the progress table created ,then to create the real task
                await sdao_ipv4.insert('taskInfo', { name: taskId.toString(), port, complete: false, paused: true, allSent: false, progress: 0, count: totoalcount })
            }

            if (type == 'port') {
                //take out all the targets and create the progress table
                var totoalcount = 0
                for (var target of selectedTargets) {
                    var re = await sdao.findone('target', { _id: target._id })
                    var lines_no = 0
                    for (var item of re.ipRange) {
                        lines_no = lines_no + 1
                        var doc = { ip: item, port }
                        await sdao_cidr.insert(taskId.toString(), doc)
                    }
                    totoalcount = totoalcount + lines_no

                }
                //create the real task
                await sdao_cidr.insert('taskInfo', { name: taskId.toString(), port, complete: false, paused, allSent: false, progress: 0, count: totoalcount })
            }

            if (type == 'combine') {
                if (stage == 'port') {
                    //take out all the targets and create the progress table
                    var totoalcount = 0
                    for (var target of selectedTargets) {
                        var re = await sdao.findone('target', { _id: target._id })
                        var lines_no = 0
                        for (var item of re.ipRange) {
                            lines_no = lines_no + 1
                            var doc = { ip: item, port: port }
                            await sdao_cidr.insert(taskId.toString(), doc)
                        }
                        totoalcount = totoalcount + lines_no

                    }
                    //create the real task
                    await sdao_cidr.insert('taskInfo', { name: taskId.toString(), port, complete: false, paused, allSent: false, progress: 0, count: totoalcount })
                }
                if (stage == 'plugin') {
                    //todo:
                    let listOfResults = await sdao_cidr.find(taskId.toString(), { 'result': { '$exists': true } })
                    var totoalcount=0
                    for (var item of listOfResults){
                        for (var ip of item){
                            var doc={ip,port}
                            totoalcount=totoalcount+1
                        }
                    }

                    //collect the result of cidr task of this task as a ipv4 target
                    //then do the same as plugin task
                }
            }
            //mark the task that the real task is created
            await sdao.update('task', { _id: taskId }, { realTaskCreating: false, realTaskCreated: true })
        }
    }, 1000)

    //dealing with the task deleted
    setInterval(async () => {
        var deletedTasks = await sdao.find('task', { deleted: true })
        for (var task of deletedTasks) {
            const {_id:taskId}=task
            await sdao_cidr.delete('taskInfo', { name: taskId.toString() })
            await sdao_cidr.dropCol(taskId.toString())
            await sdao_ipv4.delete('taskInfo', { name: taskId.toString() })
            await sdao_ipv4.dropCol(taskId.toString())
            sdao.delete('task', { _id: taskId })

        }
    }, 1000)
    //dealing with the task control changed
    setInterval(async () => {
        var changedTasks = await sdao.find('task', { synced: false })
        for (var task of changedTasks) {
            var { _id: taskId, paused } = task
            await sdao_cidr.update('taskInfo', { name: taskId.toString() }, { paused })
            await sdao_ipv4.update('taskInfo', { name: taskId.toString() }, { paused })
            await sdao.update('task', { _id: taskId }, { synced: true })
        }
    }, 1000)

    //dealing with progress collection
    setInterval(async () => {
        var progressTasks = await sdao.find('task', { start: true, paused: false, complete: false })
        for (var task of progressTasks) {
            const { _id: taskId, type, stage } = task
            if (type == 'port') {
                var info = sdao_cidr.findone('taskInfo', { name: taskId.toString() })
                const { count, progress } = info
                var percent = parseFloat(progress) / parseFloat(count) * 100
                var complete = false
                if (count == progress) complete = true
                await sdao.update('task', { _id: taskId }, { progress: percent, complete })
            }
            if (type == 'plugin') {
                var info = sdao_ipv4.findone('taskInfo', { name: taskId.toString() })
                const { count, progress } = info
                var percent = parseFloat(progress) / parseFloat(count) * 100
                var complete = false
                if (count == progress) complete = true
                await sdao.update('task', { _id: taskId }, { progress: percent, complete })
            }
            if (type == 'combine') {
                if (stage == 'port') {
                    var info = sdao_cidr.findone('taskInfo', { name: taskId.toString() })
                    const { count, progress } = info
                    var percent = parseFloat(progress) / parseFloat(count) * 100
                    percent = (percent + 0) / 2
                    var nowStage = stage
                    if (count == progress) nowStage = 'plugin'
                    //if the task completes its port stage, the percentage should be 50%, change the stage to plugin and put realTaskCreated as false
                    //so the task will be created realtask for the plugin stage
                    await sdao.update('task', { _id: taskId }, { progress: percent, stage: nowStage, realTaskCreated: false })
                }
                if (stage == 'plugin') {
                    //do the most same as plugin task
                    var info = sdao_ipv4.findone('taskInfo', { name: taskId.toString() })
                    const { count, progress } = info
                    var percent = parseFloat(progress) / parseFloat(count) * 100
                    percent = (percent + 100) / 2 //all the same except this line , because the combine task must consider the port stage process
                    var complete = false
                    if (count == progress) complete = true
                    await sdao.update('task', { _id: taskId }, { progress: percent, complete })
                }
            }
        }
    }, 1000)
    // dealing with the result collecting
    setInterval(async () => {
        var completTasks = await sdao.find('task', { complete: true, resultCollected: false })
        for (var task of completTasks) {
            var { _id: taskId, type } = task
            if (type == 'port') {
                let listOfResults = await sdao_cidr.find(taskId.toString(), { 'result': { '$exists': true } })
                let results = []
                for (var item of listOfResults)
                    results.push(...item)
                //todo:
                //save the results to file

            }
            if (type == 'plugin' || type == 'combine') {
                //todo:

            }

        }
    }, 1000)
})


