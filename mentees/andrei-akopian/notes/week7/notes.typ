#show link: underline

= Week 7

Resources dedicated to midterms and project proposal search.

== Avi Widgerson

=== Chapter 5 (cont.)

Introduces $L(f)$ as the smallest boolean formula computing a function (essentially circuit by you may not reuse wires.) He talks about history of some proof techniques related to that.

Conjecture 5.11 is interesting. Which says "there exist problems with fast sequential algorithms, but no fast parallel ones." $exists f. S(f)=O(n) and L(f)!=n^(O(1))$. Its very interesting though I didn't understand it fully.

Monotone circuits are circuits using only AND and OR gates. They can compute functions where flips from zero to 1 in the input, can produce only strictly zero to 1 flips on the output.

(so $f(0 dots 0) = 0$ and $f(1 dots 1) = 1$ and somewhere in between the $n$ flips that take $0 dots 0$ to $1 dots 1$ is line where solutions flip from zero to one.)

This sounds close to SAT, and turns out it is indeed non-polynomial. Turns out many problems are indeed pretty hard. For example perfect matching (a monotone problem) uses $n^(Omega (log n))$ gates, graph connectivity is also superpolynomial.

In 5.2.4 he covers natural proofs. Apparently the techniques used right now have the limitation that coming up with examples for them takes subexponential time, which means they will be insufficient to prove statements about "all" functions.

=== Chapter 6 Proof Complexity

After some history and Godel sorts of things I did not really understand, avi starts focusing on a particular proof system.
