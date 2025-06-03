1.2 Collisionless stellar systems 35

Figure 1.5 A field star approaches
the subject star at speed v and impact parameter b. We estimate the
resulting impulse to the subject star
by approximating the field star’s trajectory as a straight line.

and find in the notation of Figure 1.5,


Gm [2]
F ⊥ =


Gm [2] Gm [2] b

b [2] + x [2] [ cos][ θ][ =] [2] [2]


Gm [2] b

(b [2] + x [2] ) [3][/][2] [ =][ Gm] b [2] [2]


b [2]


vt
� b


� 2 � −3/2


1 +

�


. (1.28)


But by Newton’s laws

m ˙v = F so δv = [1]

m

and we have


� −∞∞


� −∞∞


dt F ⊥, (1.29)


dt

[1 + (vt/b) [2] ] [3][/][2] [ =][ Gm] bv


ds

(1.30)

(1 + s [2] ) [3][/][2] [ = 2][Gm] bv [.]


� −∞∞


δv = [Gm]

b [2]


� −∞∞


In words, δv is roughly equal to the acceleration at closest approach, Gm/b [2],
times the duration of this acceleration 2b/v. Notice that our assumption of
a straight-line trajectory breaks down, and equation (1.30) becomes invalid,
when δv ≃ v; from equation (1.30), this occurs if the impact parameter
b ∼ [< ] b 90 ≡ 2Gm/v [2] . The subscript 90 stands for a 90-degree deflection—see
equation (3.51) for a more precise definition.

Now the surface density of field stars in the host galaxy is of order
N/πR [2], where N is the number of stars and R is the galaxy’s radius, so in
crossing the galaxy once the subject star suffers

N
δn = (1.31)
πR [2] [ 2][πb][ d][b][ = 2] R [N] [2] [ b][ d][b]

encounters with impact parameters in the range b to b + db. Each such encounter produces a perturbation δv to the subject star’s velocity, but because
these small perturbations are randomly oriented in the plane perpendicular
to v, their mean is zero. [10] Although the mean velocity change is zero, the
mean-square change is not: after one crossing this amounts to


�


δv [2] ≃ δv [2] δn =


2

2Gm 2N

(1.32)

� bv � R [2] [ b][ d][b.]


10 Strictly, the mean change in velocity is zero only if the distribution of perturbing
stars is the same in all directions. A more precise statement is that the mean change
in velocity is due to the smoothed-out mass distribution, and we ignore this because the
goal of our calculation is to determine the difference between the acceleration due to the
smoothed mass distribution and the actual stars.

36 Chapter 1: Introduction

Integrating equation (1.32) over all impact parameters from b min to b max, we
find the mean-square velocity change per crossing,


ln Λ, (1.33a)

(1.33b)


� 2


Gm
� Rv


∆v [2] ≡


� b min b max


�


δv [2] ≃ 8N


where the factor


ln Λ ≡ ln


b max
� b min �


is called the Coulomb logarithm. Our assumption of a straight-line trajectory breaks down for impact parameters smaller than b 90, so we set
b min = f 1 b 90, where f 1 is a factor of order unity. Our assumption of a
homogeneous distribution of field stars breaks down for impact parameters
of order R, so we set b max = f 2 R. Then


�


ln Λ = ln


R
� b 90


+ ln(f 2 /f 1 ). (1.34)


In most systems of interest R ≫ b 90 (for example, in a typical elliptical
galaxy R/b 90 ∼ [>] 10 [10] ), so the fractional uncertainty in ln Λ arising from the
uncertain values of f 1 and f 2 is quite small, and we lose little accuracy by
setting f 2 /f 1 = 1.

Thus encounters between the subject star and field stars cause a kind
of diffusion of the subject star’s velocity that is distinct from the steady
acceleration caused by the overall mass distribution in the stellar system.
This diffusive process is sometimes called two-body relaxation since it
arises from the cumulative effect of myriad two-body encounters between
the subject star and passing field stars.

The typical speed v of a field star is roughly that of a particle in a
circular orbit at the edge of the galaxy,

v [2] ≈ [GNm] . (1.35)

R

If we eliminate R from equation (1.33a) using equation (1.35), we have


∆v [2]


. (1.36)
N


v

≈ [8 ln Λ]
v [2] N


If the subject star makes many crossings of the galaxy, the velocity v will
change by roughly ∆v [2] at each crossing, so the number of crossings n relax
that is required for its velocity to change by of order itself is given by

N
n relax ≃ (1.37)
8 ln Λ [.]

