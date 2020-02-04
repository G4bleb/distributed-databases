const DAMPING_FACTOR = 0.85;

function votes() {//Map
    //Context : "this" is a page, we are going to calculate its "votes" for its linked pages.
    page = this.value;
    for (let i = 0; i < page.adjlist.length; i++) {
        //"this" page votes using its rank for the page adjlist[i]
        emit(page.adjlist[i], page.pageRank / page.adjlist.length);
    }
    emit(this._id, 0);//Votes for itself with 0 so it is still here in case no one votes for him
    emit(this._id, page.adjlist);//Sends its links array so we don't loose it
}

function pageRankFromVotes(key, values){//Reduce
    //key : page._id, values : votes for that page
    let links;
    let totalVotes = 0;
    for (let i = 0; i < values.length; i++) {
        if(Array.isArray(values[i])){//If it's the links array
            links = values[i];
        }else{
            totalVotes += values[i];//Sum the votes
        }
    }
    let pageRank = (1 - DAMPING_FACTOR) + DAMPING_FACTOR * totalVotes;
    return {pageRank : pageRank, adjlist : links};
}

for (let i = 0; i < 20; i++) {
    db.pages.mapReduce(
        votes,
        pageRankFromVotes,
        {
            out: { replace: "pages" },
            scope: { DAMPING_FACTOR: DAMPING_FACTOR }
        }
    );
}