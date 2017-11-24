import matplotlib.gridspec as gridspec

def plot_width(df,buff=100):
    return (df.d.astype('float')>-buff)&(df.d.astype('float')<buff)

fig = plt.figure(figsize=(9.5,6))
gs = gridspec.GridSpec(2,2,height_ratios=[4,1],width_ratios=[1,1])

ax0 = plt.subplot(gs[0])
p0 = plt.scatter(
				self.basegrid.E[plot_width(self.basegrid)].tolist(),
				self.basegrid.N[plot_width(self.basegrid)].tolist(),
				s=3,
				edgecolors='none',
				)
p01 = plt.plot(
				self.basepath.E,
				self.basepath.N,
				'black',
				ls='-.',
				lw=1,
				label='s - line')
plt.legend()
ax0.set_xlabel('E (m)')
ax0.set_ylabel('N (m)')

ax1 = plt.subplot(gs[1])
p0 = plt.scatter(
				self.basegrid.s[plot_width(self.basegrid)].tolist(),
				self.basegrid.d[plot_width(self.basegrid)].tolist(),
				s=3,
				edgecolors='none',
				)
#plt.plot([0,self.basepath.Dist.max()],[0,0],'black',ls='-.',lw=1)
ax4.set_xlabel('s (m)')
ax4.set_ylabel('d (m)')
plt.show()