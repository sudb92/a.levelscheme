import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from adjustText import adjust_text
import numpy as np

nuclide="127Te"
leftlim = 1.0
rightlim = 10.0


pars = np.genfromtxt(nuclide+".dat",dtype="str")
pars = pars.T
energies = [float(par) for par in pars[0]]
spins = [str(par) for par in pars[1]]
print(energies,spins)

#energies = energies[0:8]
#spins = spins[0:8]

fig= plt.figure()
ax = fig.gca()
for energy in energies:
    p=ax.plot((leftlim,rightlim),(energy,energy),'-',color='black') #line

ax.set_ylim(np.min(energies)-50,np.max(energies)+100)
ax.set_xlim(leftlim-5,rightlim+5)
ax.set_axis_off()

texts = [ax.text(rightlim+1,energy,'%s keV'%energy, ha='left',va='center') for energy in energies]
texts2 = [ax.text(leftlim-1,energies[i],'%s'%(spins[i]), ha='right',va='center') for i in range(len(spins))]

adjtexts,_=adjust_text(
    texts,
    avoid_self=False,
    only_move="y",  # Only allow movement vertically
    max_move=None,
    ensure_inside_axes=True,
#    expand_axes=True,
    explode_radius=0.1,
    prevent_crossing=False,
    force_explode=(0.0, 0.1),
    force_pull=(0.0, 0.0),
    )

adjtexts2,_=adjust_text(
    texts2,
    avoid_self=False,
    only_move="y",  # Only allow movement vertically
    max_move=None,
    ensure_inside_axes=True,
#    expand_axes=True,
    explode_radius=0.1,
    prevent_crossing=False,
    force_explode=(0.0, 0.1),
    force_pull=(0.0, 0.0),
    )

ii = -1
for text in adjtexts:
    ii = ii + 1
    _, y_adjusted = text.get_position()
    line = Line2D(
        [rightlim+0.1, rightlim+0.3, rightlim+0.7, rightlim+0.9],
        [energies[ii], energies[ii], y_adjusted, y_adjusted],
        clip_on=False,
        linewidth=0.75,
    )
    ax.add_line(line)

ii = -1
for text in adjtexts2:
    ii = ii + 1
    _, y_adjusted = text.get_position()
    line = Line2D(
        [leftlim-0.1, leftlim-0.3, leftlim-0.7, leftlim-0.9],
        [energies[ii],energies[ii],y_adjusted,y_adjusted],
        clip_on=False,
        linewidth=0.75,
    )
    ax.add_line(line)

zsymb=''.join([s for s in nuclide if s.isalpha()])
massnum=''.join([s for s in nuclide if s.isdigit()])
print(zsymb,massnum)
formatted_nuclide = "$^{"+massnum+"}$"+zsymb
ax.text(0.5*(leftlim+rightlim), -100, formatted_nuclide,ha='center',va='center',fontsize='x-large')


gammas = np.genfromtxt(nuclide+"-gammas.dat",dtype="str")
gammas = gammas.T
begins = [float(par) for par in gammas[0]]
ends = [float(par) for par in gammas[1]]
intensities = [float(par) for par in gammas[2]]
colors = [str(par) for par in gammas[3]]
annotations = [str(par) for par in gammas[4]]

for ii in range(len(begins)):
    print(ii,begins[ii],ends[ii],intensities[ii])
    xx = ii*(rightlim-leftlim)/len(begins)+2.0
    dx = (rightlim-leftlim)/len(begins)
    yy = (begins[ii]-ends[ii])*0.5 + ends[ii]
    ax.annotate(annotations[ii],xy=(xx,yy),xycoords='data',xytext=(xx-dx*0.25,yy),textcoords='data',va='center',ha='right',rotation=90,bbox=dict(fc='white',alpha=0.8,lw=0),fontsize='x-small')
    ax.arrow(xx,begins[ii],0,ends[ii]-begins[ii],alpha=intensities[ii]*0.01,color=colors[ii],length_includes_head=True,head_width=0.2,head_length=20)

fig.tight_layout()
plt.savefig(str(nuclide)+".png")
plt.show()
