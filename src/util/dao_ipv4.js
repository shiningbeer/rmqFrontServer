var mongo = require('mongodb').MongoClient
var ObjectId = require('mongodb').ObjectId
var dao

//sync operations
const sdao = {
    connect: async (url, dbname) => {
        var err = await new Promise((resolve, reject) => {
            mongo.connect(url, { useNewUrlParser: true }, (err, db) => {
                dao = db.db(dbname)
                resolve(err)
            })
        });
        return err
    },
    dropCol: async (col) => {
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).drop((err, rest) => {
                err ? resolve(null) : resolve(rest)
            })
        });
        return re

    },


    insert: async (col, insobj) => {
        if (insobj._id != null) {
            insobj._id = ObjectId(insobj._id)
        }
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).insertOne(insobj, (err, rest) => {
                err ? resolve(null) : resolve(rest)
            })
        });
        return re
    },

    update: async (col, where, update) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var updatestr = { $set: update }
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).updateMany(where, updatestr, (err, rest) => {
                err ? resolve(null) : resolve(rest)
            })
        });
        return re
    },
    push: async (col, where, pushstr) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var updatestr = {
            $push: pushstr
        }
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).updateMany(where, updatestr, (err, rest) => {
                err ? resolve(null) : resolve(rest)
            })
        });
        return re
    },
    delete: async (col, where) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).deleteMany(where, (err, rest) => {
                err ? resolve(null) : resolve(rest)
            })
        });
        return re
    },

    findone: async (col, where = {}) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).findOne(where, (err, rest) => {
                err ? resolve(null) : resolve(rest)

            });
        });
        return re
    },
    findlimit: async (col, where = {}, limit) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).find(where).limit(limit).toArray((err, rest) => {
                err ? resolve(null) : resolve(rest)
            });
        });
        return re

    },
    findsort: async (col, where = {}, sort) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).find(where).sort(sort).toArray((err, rest) => {
                err ? resolve(null) : resolve(rest)
            });
        });
        return re

    },
    findField: async (col, where = {}, field) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).find(where, field).toArray((err, rest) => {
                err ? resolve(null) : resolve(rest)
            });
        });
        return re

    },
    find: async (col, where) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).find(where).toArray((err, rest) => {
                err ? resolve(null) : resolve(rest)
            });
        });
        return re

    },
    getCount: async (col, where = {}) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var re = await new Promise((resolve, reject) => {
            dao.collection(col).find(where).count((err, rest) => {
                err ? resolve(null) : resolve(rest)
            });
        });
        return re

    }
}

//async operations
const adao = {
    connect: (url, dbname, callback) => {
        mongo.connect(url, { useNewUrlParser: true }, (err, db) => {
            dao = db.db(dbname)
            callback(err)
        })
    },

    dropCol: (col, callback) => {
        dao.collection(col).drop((err, rest) => {
            callback(err, rest)
        })
    },


    insert: (col, insobj, callback) => {
        if (insobj._id != null) {
            insobj._id = ObjectId(insobj._id)
        }
        dao.collection(col).insertOne(insobj, (err, rest) => {
            callback(err, rest)
        })
    },

    update: (col, where, update, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var updatestr = { $set: update }
        dao.collection(col).updateMany(where, updatestr, (err, rest) => {
            callback(err, rest)
        })
    },
    push: (col, where, pushstr, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        var updatestr = {
            $push: pushstr
        }
        dao.collection(col).updateMany(where, updatestr, (err, rest) => {
            callback(err, rest)
        })
    },

    delete: (col, where, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        dao.collection(col).deleteMany(where, (err, rest) => {
            callback(err, rest)
        })
    },

    findone: (col, where = {}, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        dao.collection(col).findOne(where, (err, rest) => {
            callback(err, rest)

        });
    },
    findlimit: (col, where = {}, limit, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        dao.collection(col).find(where).limit(limit).toArray((err, rest) => {
            callback(err, rest)
        });

    },
    findsort: (col, where = {}, sort, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        dao.collection(col).find(where).sort(sort).toArray((err, rest) => {
            callback(err, rest)
        });

    },
    findField: (col, where = {}, field, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        dao.collection(col).find(where, field).toArray((err, rest) => {
            callback(err, rest)
        });

    },
    find: (col, where = {}, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        dao.collection(col).find(where).toArray((err, rest) => {
            callback(err, rest)
        });

    },
    getCount: (col, where = {}, callback) => {
        if (where._id != null)
            where._id = ObjectId(where._id)
        dao.collection(col).find(where).count((err, rest) => {
            callback(err, rest)
        });

    }
}



module.exports = {
    sdao,
    adao
}