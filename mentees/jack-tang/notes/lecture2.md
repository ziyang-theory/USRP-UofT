

$f(x)\in o(g(x)) \iff \frac{f(x)}{g(x)}\to 0$

$f(x)\in \omega(g(x)) \iff \frac{f(x)}{g(x)}\to \infty$


Define $f(x)=poly(g(x))$ as $f(x)=(g(x))^{O(1)}$

And $f(x)=\~{O}(g(x))$ as $f(x)=g(x)\cdot poly(\log g(x))$

e.g. $n^2 \log^3n\in \~O(n^2)$

e.g. $n^5 \cdot 3^n \in \~O(3^n) \ne \~O(2^n)$

When $x\to 0$ and $g(x)\to 0$, instead use $f(x)\in \~O(g(x))$ to mean $f(x)\le g(x)\cdot polylog(\frac{1}{g(x)})$

e.g. $n^2 \log\frac{1}{n}\in \~O(n^2)$

$f(x)\in \~\Omega(g(x))\iff f(x)\ge \frac{g(x)}{polylog(g(x))}$


# Harmonic Number

$H_n=1+\frac{1}{2}+\frac{1}{3}+\frac{1}{4}+\dots + \frac{1}{n}\\ \le 1+\frac{1}{2}+\frac{1}{2}+\frac{1}{4}+\frac{1}{4}+\frac{1}{4}+\frac{1}{4}+\frac{1}{8}+\frac{1}{8}+\dots \\$
$\le \lfloor\log_2 n\rfloor + 1$


$H_n \ge 1 + \frac{1}{2}+\frac{1}{4}+\frac{1}{4}+\frac{1}{8}+\frac{1}{8}+\frac{1}{8}+\frac{1}{8}+\frac{1}{16}+\dots\\$
$\ge \lceil \log_2n\rceil + 1$

Since $H_n\in O(\log n)$ and $H_n\in \Omega(\log n)$, so $H_n\in \Theta(\log n)$

<hr></hr>

Define $f(x) \sim g(x)$ as $\frac{f(x)}{g(x)}\to 1$, which is identical to $f(x)=g(x)(1+o(1))$

Prop: $H_n \sim \ln(n)$

$H_n\le 1+\int_1^n{\frac{1}{t}dt}=1+\ln n$

$H_n\ge \int_1^{n+1}{\frac{1}{t}dt}=\ln(n+1)$

<hr></hr>

$\ln (1+x) \approx x$ for small $x$

So $e^x\approx 1+x$ for small $x$

ex: $\frac{1}{1-\epsilon}\approx \frac{1}{e^{-\epsilon}}=e^\epsilon \approx 1+\epsilon$

<br/>

$a+b\approx \max(a,b)$ since $\max(a,b)\le a+b\le 2\max(a,b)$


