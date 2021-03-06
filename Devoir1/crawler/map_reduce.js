db.spells.mapReduce(
    function () { emit(this.name, 1); },
    function (key, values) {
        return values;
    }
    ,
    {
        query: { $and: [{ "level.sorcerer/wizard": { $lte: 4 } }, { components: ["V"] }] },
        out: "usable_spells"
    }
)

db.spells.find({ $and: [{ "level.sorcerer/wizard": { $lte: 4 } }, { components: ["V"] }] })