import osqp
import numpy as np
from scipy import sparse
import math
import matplotlib.pyplot as plt
# Discrete time model of a quadcopter

# Initial and reference states  

xr = np.array([2,6,0*math.pi/180])
x0 = np.array([0,0,math.atan2(xr[1],xr[0])])


# Simulate in closed loop
nsim = 2000
dt=0.01
xp=[]
yp=[]
thp=[]
xp.append(x0[0])
yp.append(x0[1])
# Objective function
Q = sparse.diags([1, 1, 0])
QN = Q
R = 0.1*sparse.eye(2)



for i in range(nsim):

# Prediction horizon
    N = 50
# Ax+Bu
    Ad = sparse.csc_matrix([
    [1.,      0.,     0],
    [0.,      1.,     0],
    [0.,      0.,     1],
    ])

    Bd = sparse.csc_matrix([
    [math.cos(x0[2])*0.01,     0],
    [math.sin(x0[2])*0.01,     0],
    [0,  0.01]
    ])
     
    [nx, nu] = Bd.shape
    # Constraints 
    u0 = np.array([0, 0])
    umin = np.array([-0.4, -0.4])-u0
    umax = np.array([0.4, 0.4])-u0 
    xmin = np.array([-10,-10,-10])
    xmax = np.array([10, 10, 10])
# Cast MPC problem to a QP: x = (x(0),x(1),...,x(N),u(0),...,u(N-1))
# - quadratic objective
    P = sparse.block_diag([sparse.kron(sparse.eye(N), Q), QN,
                        sparse.kron(sparse.eye(N), R)], format='csc')                    
# - linear objective
    q = np.hstack([np.kron(np.ones(N), -Q.dot(xr)), -QN.dot(xr),
               np.zeros(N*nu)])

# - linear dynamics
    Ax = sparse.kron(sparse.eye(N+1),-sparse.eye(nx)) + sparse.kron(sparse.eye(N+1, k=-1), Ad)
    Bu = sparse.kron(sparse.vstack([sparse.csc_matrix((1, N)), sparse.eye(N)]), Bd)
    Aeq = sparse.hstack([Ax, Bu])
    leq = np.hstack([-x0, np.zeros(N*nx)])
    ueq = leq
# - input and state constraints
    Aineq = sparse.eye((N+1)*nx + N*nu)
    lineq = np.hstack([np.kron(np.ones(N+1), xmin), np.kron(np.ones(N), umin)])
    uineq = np.hstack([np.kron(np.ones(N+1), xmax), np.kron(np.ones(N), umax)])
# - OSQP constraints
    A = sparse.vstack([Aeq, Aineq], format='csc')
    l = np.hstack([leq, lineq])
    u = np.hstack([ueq, uineq])

# Create an OSQP object
    prob = osqp.OSQP()

# Setup workspace
    prob.setup(P, q, A, l, u, warm_start=True)
    # Solve
    res = prob.solve()

    # Check solver status
    if res.info.status != 'solved':
        raise ValueError('OSQP did not solve the problem!')

    # Apply first control input to the plant
    ctrl = res.x[-N*nu:-(N-1)*nu]
    x=x0[0] + dt*ctrl[0]*math.cos(x0[2])
    y=x0[1] + dt*ctrl[0]*math.sin(x0[2])
    theta=x0[2]+dt*ctrl[1]
    x0[0] = x
    x0[1] = y
    x0[2] = theta   
    xp.append(x)
    yp.append(y)
    thp.append(theta*180/math.pi)
    


plt.figure(1)
plt.title('x')
plt.plot(xp)
plt.figure(2)
plt.title('y')
plt.plot(yp)
plt.figure(3)
plt.title('theta')
plt.plot(thp)
plt.show()
