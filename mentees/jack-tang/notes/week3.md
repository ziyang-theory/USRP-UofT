# CS Theory Toolkit (lec 4)

To standardize variable:

* Mean 0: subtrack mean $\mu =E[X]$
* Stdev 1: divide by stdev $\sigma=\sqrt{Var(X)}= \sqrt{E(X-E[X])^2}$

So the standardized $\frac{X-E[X]}{\sqrt{E[X^2]-E[X]^2}}$<br>
In general. define the standardized variable $Z=\frac{X-\mu}{\sigma}$<br>
_Constant variables (var=0) are not standardizable!_

Suppose $z=(z_1, z_2, \dots, z_n)$ where each $z_i$ is independent with each other and from an identical standard gaussian distribution. Then the distribution of $z$ is rotationally symmetric. 

# Turing's Paper

Machine reads, then write or erase, and then move left or right on the tape.

<br>

* Automatic Machine: action determined completely by configuration

* Choice Machine: action partially determined by configuration; contribution from external operator

    * "This would be the case if we were using machines to deal with axiomatic systems". _What are axiomatic systems?_

<br>

**"If a computing machine never writes down more than a finite number of symbols of the first kind, it will be called circular. Otherwise it is said to be circle-free."**

**"A sequence is said to be computable if it can be computed by a circle-free machine. A number is computable if it differs by an integer from the number computed by a circle-free machine."**

_What are some uncomputable sequences/numbers?_<br>
\- irrational numbers, for they require infinite prints<br>
\- *are all finite sequences computable?? since just take a tape that literally records it*

<br>

Turing uses a simplification of configuration tables by allowing multiple chains of actions at each configuration.<br>
_Is this justifed?_<br>
I think so, just create a helper chain of configurations that acts out the behaviour. So the notation is valid shorthand.









