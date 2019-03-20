namespace HousePriceAnalysis

module Statistics =
    open MathNet.Numerics.Statistics
    open System.Linq

    let Quantiles(n:int)(dataSet:seq<float>) = 
        let quantileMarks = seq {for i in 0 .. n do yield (float i/float n)}
        let quantiles : float[] = quantileMarks |> Seq.map (fun t -> Statistics.Quantile(dataSet,t)) |> Seq.toArray
        quantiles
    
    let QuantilesBy(selector:'a->float)(n:int)(dataSet:seq<'a>) =
        dataSet |> Seq.map selector |> Quantiles(n)

    let Quantile(i:int)(n:int)(dataSet:seq<float>) =
        Statistics.Quantile(dataSet,(float i)/(float n))

    let QuantileBy(selector:'a->float)(i:int)(n:int)(dataSet:seq<'a>) =
        dataSet |> Seq.map selector |> Quantile(i)(n)

    let InterQuartileRangeBy(selector:'a->float)(dataSet:seq<'a>) =
        dataSet |> Seq.map selector |> (fun f -> Quantile(1)(4)(f)-Quantile(3)(4)(f))

    let Winsorise(ntile:int)(values:seq<float>) = 
        let quantiles = values |> Quantiles(ntile) 
        values |> Seq.filter (fun v -> v>quantiles.[1] && v<quantiles.[ntile])

    let WinsoriseBy(ntile:int)(selector:'T->float)(items:seq<'T>) = 
        let values = items |> Seq.map (fun i -> (i,selector(i)))
        let quantiles = values |> Seq.map (fun (i,v) -> v) |> Quantiles(ntile) 
        values |> Seq.filter (fun (i,v) -> v>quantiles.[1] && v<quantiles.[ntile]) |> Seq.map (fun (i,v) -> i)

    let MatchBands(n:int)(values:seq<float>) = 
        let bands = values |> Quantiles(10)
        let boxes = bands |> Seq.map (fun b -> ((bands |> Seq.findIndex((fun i -> i=b))),b))
        values |> Seq.map (fun v -> boxes.Last(fun (i,b) -> v>b)) |> Seq.map (fun (i,b) -> i)

    let CollateBy(collater:'a -> 'b)(collation:seq<'a>->float)(dataSet:seq<'a>) =
//        let distinctKeys = dataSet.Select(collater).Distinct()
//        distinctKeys |> Seq.map (fun k -> (k,collation(dataSet.Where(fun d -> collater(d)=k))))
        dataSet |> Seq.groupBy collater |> Seq.map (fun (k,g) -> (k,g |> collation))