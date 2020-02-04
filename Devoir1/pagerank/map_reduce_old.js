var currColl = db.getCollection("initialdata");
const DAMPING_FACTOR = 0.85;

function votes() {//Map
    //Context : this" is the current page whose pagerank we're calculating.
    pagesThatLinkHere = db.initialdata.find({adjlist : this._id});
    emit(this._id, pagesThatLinkHere.map(p => p.pageRank / p.adjlist.length));
}

function pageRankFromVotes(key, values){//Reduce
    let pageRank = (1 - DAMPING_FACTOR) + DAMPING_FACTOR * Array.sum(values);
    let thisPage = db.initialdata.findOne({_id : key});
    return {pageRank : pageRank, adjlist : thisPage.adjlist};
}

currColl.mapReduce(
    votes,
    pageRankFromVotes,
    {
        out: "it_1",
        query: { },
        scope: { DAMPING_FACTOR: DAMPING_FACTOR}
    }
)