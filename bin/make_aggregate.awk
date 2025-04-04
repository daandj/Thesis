BEGIN {state = ""; aggregate = 0 }
/Means/ { state = "Means" }
/Results/ { state = "Results" }
!/Results/ || /Means/ {
    if (state == "Means") {
        if (means_out) {
            print $0 > means_out
        }
    } else if (state == "Results") {
        aggregate += $2
        avg_wins = aggregate/($1+1)
        print $1 "\t" avg_wins
    }
}
