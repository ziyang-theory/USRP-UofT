# Finite fields and additive secret sharing

At the [October 16, 2026 meeting](../meetings/2026-10-16.md), we discussed how three people can compute the sum of their ages with additive shares. The numbers in the worked example here are for illustration.

## Arithmetic in a finite field

A **field** is a set with addition and multiplication that obey the associative, commutative, and distributive laws. It has distinct identity elements $0$ for addition and $1$ for multiplication. Every element has an additive inverse, and every nonzero element has a multiplicative inverse. A **finite field** has finitely many elements.

For a prime $p$, the integers modulo $p$ form the field $\mathbb{F}_p$. We represent its elements by $0,1,\ldots,p-1$ and reduce arithmetic results modulo $p$. For example, in $\mathbb{F}_7$,

$$
5+4=2,\qquad 3\cdot5=1,\qquad 3^{-1}=5.
$$

Here $5+4=2$ means that $9$ has remainder $2$ on division by $7$. Division by $3$ means multiplication by $5$.

This construction requires a prime $p$. Arithmetic modulo $6$ does not form a field because the nonzero element $2$ has no multiplicative inverse.

Prime fields are sufficient for this example. Other constructions give finite fields whose sizes are powers of primes.

### A field with four elements

The field $\mathbb{F}_4$ has $4=2^2$ elements:

$$
\mathbb{F}_4=\{0,1,\alpha,\alpha+1\}.
$$

Each element has the form $a+b\alpha$, where $a,b\in\mathbb{F}_2$. We introduce the new element $\alpha$ with the multiplication rule

$$
\alpha^2=\alpha+1.
$$

To add elements, add their coefficients modulo $2$. Since $1+1=0$, every element added to itself gives $0$. For example,

$$
\alpha+\alpha=0,\qquad
(\alpha+1)+\alpha=1,\qquad
(\alpha+1)+1=\alpha.
$$

To multiply elements, expand the product, reduce its coefficients modulo $2$, and replace $\alpha^2$ with $\alpha+1$. For example,

$$
\alpha(\alpha+1)=\alpha^2+\alpha=(\alpha+1)+\alpha=1.
$$

Also,

$$
(\alpha+1)^2=\alpha^2+\alpha+\alpha+1
=\alpha^2+1=\alpha.
$$

| $\cdot$ | $0$ | $1$ | $\alpha$ | $\alpha+1$ |
| --- | --- | --- | --- | --- |
| $0$ | $0$ | $0$ | $0$ | $0$ |
| $1$ | $0$ | $1$ | $\alpha$ | $\alpha+1$ |
| $\alpha$ | $0$ | $\alpha$ | $\alpha+1$ | $1$ |
| $\alpha+1$ | $0$ | $\alpha+1$ | $1$ | $\alpha$ |

Every nonzero element has an inverse:

$$
1^{-1}=1,\qquad
\alpha^{-1}=\alpha+1,\qquad
(\alpha+1)^{-1}=\alpha.
$$

Polynomial arithmetic supplies the associative, commutative, and distributive laws. Together with these inverses, the rules give a field.

Arithmetic modulo $4$ does not give this field. Modulo $4$, the nonzero element $2$ satisfies $2\cdot2=0$ and has no multiplicative inverse. In $\mathbb{F}_4$, the coefficients are modulo $2$, even though the field has four elements.

The age-sum protocol below uses a larger prime field to recover the ordinary integer total.

## Splitting a value into additive shares

To share $x\in\mathbb{F}_p$ among three participants, choose $r_1,r_2$ independently and uniformly from $\mathbb{F}_p$. Then set

$$
r_3=x-r_1-r_2.
$$

Give participant $j$ the share $r_j$. All three shares reconstruct the value:

$$
r_1+r_2+r_3=x.
$$

Any fixed pair of shares is uniformly distributed over $\mathbb{F}_p^2$, independently of $x$. For example, fix any proposed values of $r_1,r_3$ and any secret $x$. Exactly one choice of $r_2$ completes the equation. Thus, that pair occurs with probability $1/p^2$ for every $x$. The same reasoning applies to the other pairs.

This is **3-out-of-3 additive secret sharing**: any two shares alone reveal no information about the secret.

Choose fresh, independent random values for every new sharing. Shares are field elements, so their values do not need to be plausible ages.

## Three-party computation of an age sum

Let Alice, Bob, and Charlie hold integer ages $a,b,c$. Everyone should receive the total $S=a+b+c$.

Assume that everyone follows the protocol and sends shares through private, authenticated channels. These channels keep each share private to its recipient and identify its sender.

For the privacy discussion, consider one participant who follows the instructions but records everything they see. This is the **semi-honest** model with one curious participant.

Assume each age is between $0$ and a public upper bound $M$. Choose a prime $p>3M$ so that the total is less than $p$. Reconstruction modulo $p$ then gives the ordinary integer sum without wraparound.

1. Alice samples $a_1,a_2$ independently and uniformly from $\mathbb{F}_p$, then sets $a_3=a-a_1-a_2$. Bob and Charlie do the same for their ages. Each person keeps the share for their own position and privately sends the other two shares to their recipients.
2. Each participant adds the shares they hold. Alice computes $t_1=a_1+b_1+c_1$, Bob computes $t_2=a_2+b_2+c_2$, and Charlie computes $t_3=a_3+b_3+c_3$.
3. Each participant sends their $t_j$ to both others. Everyone computes $t_1+t_2+t_3$ modulo $p$.

Correctness follows by rearranging the sums:

$$
t_1+t_2+t_3
=(a_1+a_2+a_3)+(b_1+b_2+b_3)+(c_1+c_2+c_3)
=a+b+c.
$$

The participants reveal their shares of the total and keep the individual input shares private.

### Worked example

For this example, assume all ages are at most $30$ and use $p=101>90$. For ages $20,21,22$, one possible set of shares is:

| Input owner | Age | Share held by Alice | Share held by Bob | Share held by Charlie |
| --- | ---: | ---: | ---: | ---: |
| Alice | 20 | 37 | 80 | 4 |
| Bob | 21 | 92 | 15 | 15 |
| Charlie | 22 | 8 | 61 | 54 |
| Column sum modulo 101 | | 36 | 55 | 73 |

Each row sums to its owner's age modulo $101$. The participants reveal $36,55,73$ and compute

$$
36+55+73=164\equiv63\pmod{101},
$$

which equals $20+21+22$. During the protocol, each participant knows their own row and column. The full table is visible here for teaching.

### What privacy means here

Alice knows her own age $a$ and learns the total $S$, so she learns $b+c=S-a$. Her complete view includes her input, random choices, and messages. Privacy means that this view gives no additional information about Bob's and Charlie's ages beyond her own age and the total.

Consider any two pairs $(b,c)$ and $(b',c')$ with the same sum. Alice's view has the same distribution for both pairs. The same statement holds for Bob and Charlie.

The privacy intuition is that Alice receives uniform shares. The unrevealed random shares hide Bob's and Charlie's individual contributions to the announced column sums. The reconstruction equation above establishes correctness separately.

If two participants combine their ages and the total, they can calculate the third age. That information already follows from the chosen output.

The procedure assumes that participants follow its steps. Someone who sends an incorrect share of the total can change the answer. Additional mechanisms are necessary to handle such deviations.

For more background, see Evans, Kolesnikov, and Rosulek's [*A Pragmatic Introduction to Secure Multi-Party Computation*, Section 3.4, p. 46](https://securecomputation.org/docs/pragmaticmpc.pdf#page=47). This section covers additive sharing and local addition of shared values. The book was published in 2018, and the linked version is dated June 11, 2022.

## Questions for review

- Why must the random shares range over the whole field, even when ages lie in a small interval?
- What could go wrong if the modulus were smaller than the largest possible total?
- Why do participants reveal column sums instead of revealing every share?

The [meeting notes](../meetings/2026-10-16.md#question-to-think-about) contain the separate probability question for next week's discussion.
