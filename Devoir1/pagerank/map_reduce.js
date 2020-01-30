

db.initaldata.mapReduce(
    function () {//Map
        emit(this.name, 1);
    },
    function (key, values) {//Reduce
        values;
    },
    {
        query: { $and: [{ "level.sorcerer/wizard": { $lte: 4 } }, { components: ["V"] }] },
        out: "usable_spells"
    }
)