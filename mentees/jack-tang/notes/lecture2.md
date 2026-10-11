

$f(x)\in o(g(x)) \iff \frac{f(x)}{g(x)}\to 0$

$f(x)\in \omega(g(x)) \iff \frac{f(x)}{g(x)}\to \infty$


Define $f(x)=poly(g(x))$ as $f(x)=(g(x))^{O(1)}$

And $f(x)=\~{O}(g(x))$ as $f(x)=g(x)\cdot poly(\log g(x))$

e.g. $n^2 \log^3n\in \~O(n^2)$

e.g. $n^5 \cdot 3^n \in \~O(3^n) \ne \~O(2^n)$

When $x\to 0$ and $g(x)\to 0$, instead use $f(x)\in \~O(g(x))$ to mean $f(x)\le g(x)\cdot polylog(\frac{1}{g(x)})$

e.g. $n^2 \log\frac{1}{n}\in \~O(n^2)$

$f(x)\in \~\Omega(g(x))\iff f(x)\ge \frac{g(x)}{polylog(g(x))}$



