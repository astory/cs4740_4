#!/usr/local/bin/perl
# NOTE: this has only been tested on solaris machines.  In particular
# there is an imbedded sort that may not work on other machines.

# pp_eval.pl Perl script to evaluate a single QA track run using
#     Perl patterns to decide correctness of answer string
# Usage: pp_eval.pl patterns submission
#     where patterns is the name of the file containing the Perl patterns
#     and   submission is the name of the file containing to be evaluated
# Evaluation is the mean reciprocal rank of the first correct response.
# A response is counted as correct if some pattern for the current
# question has a string match with the response.
# Submission files are of the form
#    qid Q0 docno rank score tag response
# Output: score for each question and mean over all questions 

$#ARGV==1 || die "Usage: pp_eval.pl patterns submission\n";
$patterns = $ARGV[0];
$submission = $ARGV[1];

if ( (! -e $patterns) || (! open PATTERNS, "<$patterns") ) {
    die "Can't find/open patterns file `$patterns': $!\n";
}
while ($line = <PATTERNS>) {
    chomp $line;
    ($qid, $pattern) = split " ", $line, 2;
    push @{$patterns[$qid]}, $pattern;
}
close PATTERNS || die "can't close pattern file: $!\n";

# process submission file in sorted order
if ( (! -e $submission) ||
     (! open INPUT, "sort +0 -1n +3 -4n $submission |") ) {
    die "Can't find/open/sort submission file `$submission': $!\n";
}
$oldq = -1;
$sum = 0;
$num_notfound = 0;
$num_qs = 0;
while ($line = <INPUT>) {
    chomp $line;
    ($qid, $q0, $docno, $given_rank, $score, $tag, $response) =
		split " ", $line, 7;
    next if ($qid == 131 || $qid == 184);

    if ($qid != $oldq) {
	# print oldq's score and add to running sum for average
	# re-initialize for current qid
	if ($oldq != -1) { # i.e., not very first query
	    if ($answer_rank != 0) { # had a correct answer
		$recip = 1 / $answer_rank;
	        printf "Question %3d: Correct answer found at rank %d (%.2f).\n",
			$oldq, $answer_rank, $recip;
		$sum += $recip;
	    }
	    else { 
	        printf "Question %3d: No correct answer found. \n", $oldq;
		$num_notfound++;
	    }
	}
	$rank = 0;
	$answer_rank = 0;
	$num_qs++;
	$oldq = $qid;
    }

    $rank++;    # make sure ranks are 1-5, not 0-4
    if (0 == $answer_rank) { # if still looking for a correct answer
        foreach $p (@{$patterns[$qid]}) {
	    if ($response =~ /(?:\W|^)$p(?:\W|$)/i) {
		$answer_rank = $rank;
		last;
	    }
	}
    }
}
if ($qid != 0) { # i.e., submission file not empty
    if ($answer_rank != 0) { # last question had a correct answer
	$recip = 1 / $answer_rank;
        printf "Question %3d: Correct answer found at rank %d (%.2f).\n",
		$qid, $answer_rank, $recip;
	$sum += $recip;
    }
    else { 
        printf "Question %3d: No correct answer found. \n", $oldq;
		$num_notfound++;
    }
}

$ave = $sum / $num_qs;
printf "\nMean reciprocal rank over %d questions is %.3f\n", $num_qs, $ave;
print "$num_notfound questions had no answers found in top 5 responses.\n";


