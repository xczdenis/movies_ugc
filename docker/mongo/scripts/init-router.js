function addShard(replSetName, shardName) {
    sh.addShard(`${replSetName}/${shardName}`);
    console.log(`The following replSet/shard has been added: ${replSetName}/${shardName}`);
}

const mongoCluster = [
    {
        replSet: "rs-shard-01",
        nodes: [
            "mongo-shard01-a:27017",
            "mongo-shard01-b:27017",
            "mongo-shard01-c:27017"
        ]
    },
    {
        replSet: "rs-shard-02",
        nodes: [
            "mongo-shard02-a:27017",
            "mongo-shard02-b:27017",
            "mongo-shard02-c:27017"
        ]
    }
]

mongoCluster.forEach((cluster) => {
    cluster.nodes.forEach((node) => {
        addShard(cluster.replSet, node);
    })
})

