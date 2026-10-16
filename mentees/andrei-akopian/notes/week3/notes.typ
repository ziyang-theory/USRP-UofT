= Week 3

=== Lecture 3c

Approximation of binomial combinatorics.

After generic logarithm and other approximation tricks. Then he does $k = p n$ and starts doing cdf sort of things.

Then he uses that $(x+1)^n$ to say that first $k$ binomial terms summated are $>= x^k dot V(n,k)$ for a lower bound. $V(n,k) <= ((1+x)/x^p)^n$.

The nice things about these expressions, is that if $0<=x<=1$ then they behave pretty well.

After a bunch more rearrangements, he gets a nice expression for $V$ in terms of $p$. Which is nicely related to entropy, because it describes how much information is stored in the choice permutations.

He finishes by applying the stirling approximation. $sqrt(2 pi n) (n^n)/e^(n)$ to obtain a very similar value to the above, off only by a constant factor.

=== Recitation 2

O'Donnel tries to analyze a few strange sequences. Common tricks are to punch it into mathematica, try to make it look like $e$ to some power. Sometimes it is good to assume it is similar to a different nicer to work with function and proceed working with that one.

The techniques amount to repeatedly switching between logarithm and exponent of a number, constantly trying calculus techniques against these forms, checking either for convergence, or asymptotic similarity to some other function. At some point nice solution will appear which you can go back and improve or check that it is a bound.

A lot of scientific hypothesis etc. tricks work pretty well.

=== (Unrelated) Prime Magic

When analyzing prime numbers in a set of numbers [0,n], it can be assumed that primes are independently destributed (which they almost are).

And then nicely the number of numbers that have $p_1$ as a factor will be $n/p_1$ and if additionally $p_2$ that will be $n/(p_1 p_2)$ etc. All very nice to work with.

=== Lecture 4ab

Explain the motivation behind the gaussian distributions. The main thing is that adding multiple gaussians together also gives a gaussian. (Take a lot of $plus.minus 1$.) By the central limit theorem, any sum of independent distributions will end up looking like a gaussian.

Most important fact about gaussians: Take a vector of samples from a gaussian $N(0,1)$. They will be rotationally symetrical. i.e. orthogonal transformations will produce gaussians with the same probability.

Sum of independent gaussians is a gaussian. This is also important.

Then this curious fact from #link("https://www.3blue1brown.com/lessons/clt/")[3 blue 1 brown] about the integral of a gaussian distribution having a constant of $sqrt(2 pi)$.

=== Lecture 4c

Berry Esseen Theorem. Bounds the error of pdf (integral) of a gaussian distribution (see #link("https://en.wikipedia.org/wiki/Normal_distribution#/media/File:Normal_Distribution_CDF.svg")[Cumulative Distribution Function] to a constant factor of $sum_(i=1)^n E[|X_i|^3]$

I didn't really understand the justification. Will have to come back to it.
