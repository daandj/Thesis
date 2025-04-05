BEGIN { aggregate = 0 }
{
    aggregate += $2
    avg_wins = aggregate/($1+1)
    print $1 "\t" avg_wins
}
