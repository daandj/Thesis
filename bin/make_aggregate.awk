BEGIN {state = ""; aggregate = 0 }
/Means/ { state = "Means" }
/Results/ { state = "Results" }
!/Results/ || /Means/ {
    if (state == "Means") {
    } else if (state == "Results") {
        aggregate += $2
        print $1 "\t" aggregate
    }
}
