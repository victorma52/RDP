import numpy as np
import matplotlib.pyplot as plt
#inputs for model (all units in cgs)
pitch=float(input("Input Lattice Pitch (cm)"));
pufraction=float(input("Input Plutonium Fraction (%)"))/100;
fuel_length=float(input("Input Fuel Element Length (cm)"));
coreDia=float(input("Input Reactor Core Diameter (cm)"));
#Core and Cell Volume
Vcell=((pitch)**2)*fuel_length;
Vcore=((1/4)*(np.pi)*(0.5*coreDia))*fuel_length;
#Fuel Volume
fuelD=0.9;
Vfuel=((1/4)*np.pi*(fuelD)**2)*fuel_length;

#Cladding Volume
Cladthick=0.05
Vclad=(np.pi/4)*(((fuelD+(2*Cladthick))**2)-(fuelD)**2)*fuel_length;

#Coolant Volume
Vcool=Vcell-Vfuel-Vclad;

#Simple Averaging Fractions
fuelfraction=(Vfuel/Vcell);
cladfraction=(Vclad/Vcell);
coolfraction=(Vcool/Vcell);

#Fuel Composition Fractions (Plutonium Fraction is pufraction)
ufraction=1-pufraction

#Densities of Lattice Materials (SS316 cross section approximated with elemental iron)
N_a=6.02e+23;
SS316_density=8;
Na_density=0.927;
Fuel_density=19;

#Molar Mass of Lattice Materials
MM_SS316=55.85;
MM_Na=22.99;
MM_U=238;
MM_Pu=239;

#Number Densities of Lattice Materials
N_SS316=(SS316_density)*(N_a/MM_SS316);
N_Na=(Na_density)*(N_a/MM_Na);
N_U=(1-pufraction)*(Fuel_density)*(N_a/MM_U);
N_Pu=(pufraction)*(Fuel_density)*(N_a/MM_Pu);
barns=1e-24

#Macroscopic 8-group Cross Sections of Sodium Coolant
microNaNS=np.array([[1.5,2.2,3.6,3.5,4.0,3.9,7.3,3.2],
               [0.0050,0.0002,0.0004,0.0010,0.0010,0.0010,0.0090,0.0080],
               [0,0,0,0,0,0,0,0],
               [0.623,0.6908,0.4458,0.2900,0.3500,0.3000,0.0400,0],
               [0,0,0,0,0,0,0,0]]).T;

microNaS=np.array([[0,0.52,0.09,0.003,0.009,0.001,0,0],
                   [0,0,0.69,0,0.0004,0.0004,0,0],
                   [0,0,0,0.44,0.005,0.008,0,0],
                   [0,0,0,0,0.29,0,0,0],
                   [0,0,0,0,0,0.35,0,0],
                   [0,0,0,0,0,0,0.3,0],
                   [0,0,0,0,0,0,0,0.04],
                   [0,0,0,0,0,0,0,0]]);

macroNaNS=N_Na*barns*microNaNS;
macroNaS=N_Na*barns*microNaS;

#Macroscopic 8-group Cross Sections of SS316 (Iron)
microFeNS=np.array([[2.2,2.1,2.4,3.1,4.5,6.1,6.9,10.4],
                    [0.02,0.003,0.005,0.006,0.008,0.012,0.032,0.02],
                    [0,0,0,0,0,0,0,0],
                    [1.0108,0.46,0.12,0.14,0.28,0.07,0.04,0],
                    [0,0,0,0,0,0,0,0]]).T;

microFeS=np.array([[0,0.75,0.2,0.05,0.01,0.0008,0,0],
                    [0,0,0.33,0.1,0.02,0.01,0,0],
                    [0,0,0,0.12,0,0,0,0],
                    [0,0,0,0,0.14,0,0,0],
                    [0,0,0,0,0,0.28,0,0],
                    [0,0,0,0,0,0,0.07,0],
                    [0,0,0,0,0,0,0,0.04],
                    [0,0,0,0,0,0,0,0]]);

macroFeNS=N_SS316*barns*microFeNS;
macroFeS=N_SS316*barns*microFeS;

#Macroscopic 8-group Cross Sections of U-238
microUNS=np.array([[4.3,4.8,6.3,9.3,11.7,12.7,13.1,11],
                   [0.01,0.09,0.11,0.15,0.26,0.47,0.84,1.47],
                   [0.58,0.2,0,0,0,0,0,0],
                   [2.293,1.49,0.3759,0.2935,0.2,0.09,0.01,0],
                   [2.91,2.58,0,0,0,0,0,0]]).T;

microUS=np.array([[0,1.28,0.78,0.2,0.03,0.003,0,0],
                  [0,0,1.05,0.42,0.01,0.01,0,0],
                  [0,0,0,0.33,0.04,0.005,0.009,0],
                  [0,0,0,0,0.29,0.003,0.005,0],
                  [0,0,0,0,0,0.18,0.02,0],
                  [0,0,0,0,0,0,0.09,0],
                  [0,0,0,0,0,0,0,0.01],
                  [0,0,0,0,0,0,0,0]]);

macroUNS=N_U*barns*microUNS;
macroUS=N_U*barns*microUS;

#Macroscopic 8-group Cross Sections of Pu-239
microPuNS=np.array([[4.5,5.1,6.3,8.6,11.3,13.1,16.5,31.8],
                    [0.01,0.03,0.11,0.2,0.35,0.59,1.98,8.54],
                    [1.85,1.82,1.6,1.51,1.6,1.67,2.78,10.63],
                    [1.49,0.826,0.3709,0.1905,0.15,0.09,0.01,0],
                    [3.4,3.07,2.95,2.9,2.88,2.88,2.87,2.87]]).T;

microPuS=np.array([[0,0.66,0.6,0.19,0.04,0.005,0,0],
                   [0,0,0.64,0.15,0.03,0.006,0,0],
                   [0,0,0,0.31,0.05,0.01,0.009,0],
                   [0,0,0,0,0.18,0.01,0.005,0],
                   [0,0,0,0,0,0.13,0.02,0],
                   [0,0,0,0,0,0,0.09,0],
                   [0,0,0,0,0,0,0,0.01],
                   [0,0,0,0,0,0,0,0]]);

macroPuNS=N_Pu*barns*microPuNS;
macroPuS=N_Pu*barns*microPuS;

#Fission,Capture,and Absorbtion 8-group Cross Sections of Sodium Coolant
fissNa=macroNaNS[:,2];
capNa=macroNaNS[:,1];
abspNa=fissNa+capNa;

#Fission,Capture,and Absorbtion 8-group Cross Sections of SS316
fissFe=macroFeNS[:,2];
capFe=macroFeNS[:,1];
abspFe=fissFe+capFe;

#Fission,Capture,and Absorbtion 8-group Cross Sections of U-238
fissU=macroUNS[:,2];
capU=macroUNS[:,1];
abspU=fissU+capU;

#Fission,Capture,and Absorbtion 8-group Cross Sections of Pu-239
fissPu=macroPuNS[:,2];
capPu=macroPuNS[:,1];
abspPu=fissPu+capPu;

#Transport 8-group Cross Sections of all Core Materials
trNa=macroNaNS[:,0];
trFe=macroFeNS[:,0];
trU=macroUNS[:,0];
trPu=macroPuNS[:,0];

#Removal 8-group Cross Sections of all Core Materials
reNa=macroNaNS[:,3]+abspNa;
reFe=macroFeNS[:,3]+abspFe;
reU=macroUNS[:,3]+abspU;
rePu=macroPuNS[:,3]+abspPu;

#Fission Neutron Production of all Core Materials (vSigmaF)
vfNa=microNaNS[:,4]*fissNa;
vfFe=microFeNS[:,4]*fissFe;
vfU=microUNS[:,4]*fissU;
vfPu=microPuNS[:,4]*fissPu;    

#Simple Cell Homogenization of Transport Cross Sections 
trCellg=(trNa*coolfraction)+(trFe*cladfraction)+(trU*fuelfraction)+(trPu*fuelfraction);

#Simple Cell Homogenization of Absorbtion Cross Sections 
abspCellg=(abspNa*coolfraction)+(abspFe*cladfraction)+(abspU*fuelfraction)+(abspPu*fuelfraction);

#Simple Cell Homogenization of Removal Cross Sections 
reCellg=(reNa*coolfraction)+(reFe*cladfraction)+(reU*fuelfraction)+(rePu*fuelfraction);

#Simple Cell Homogenization of Downscattering Cross Sections
dsCellg=(macroNaS*coolfraction)+(macroFeS*cladfraction)+(macroUS*fuelfraction)+(macroPuS*fuelfraction);

#Simple Cell Homogenization of Fission Cross Sections 
fissCellg=((fissNa*coolfraction)+(fissFe*cladfraction)+(fissU*fuelfraction)+(fissPu*fuelfraction));

#Simple Cell Homogenization of Fission Neutron Production (vSigmaF) 
vfCellg=(vfNa*coolfraction)+(vfFe*cladfraction)+(vfU*fuelfraction)+(vfPu*fuelfraction);

#8-group Diffusion Coefficients of Homogenized Cell
Dg=1/(3*(trCellg+abspCellg));
    
#8-group Fission Spectrum
Xg=np.array([[0.365,0.396,0.173,0.050,0.012,0.003,0.001,0]]).T;

#Buckling Variable and Eigenvalue for Keff=1.15
extr=20;
B=((2.405/((0.5*coreDia)+extr))**2)+(((np.pi)/(fuel_length+(2*extr)))**2);

#Constructing Matricies to Find Keff
fissionMatrix=np.asmatrix(np.array([vfCellg])).T;
fixedScatterArray=dsCellg.T

scatterMatrix=np.asmatrix(fixedScatterArray);

diffusionMatrix=np.asmatrix(np.array([Dg])).T;
DBgMatrix=B*diffusionMatrix;
reMatrix=np.asmatrix(np.array([reCellg])).T;
DBgReMatrix=(DBgMatrix+reMatrix);

M=np.matrix([[DBgReMatrix[0,0],0,0,0,0,0,0,0],
             [0,DBgReMatrix[1,0],0,0,0,0,0,0],
             [0,0,DBgReMatrix[2,0],0,0,0,0,0],
             [0,0,0,DBgReMatrix[3,0],0,0,0,0],
             [0,0,0,0,DBgReMatrix[4,0],0,0,0],
             [0,0,0,0,0,DBgReMatrix[5,0],0,0],
             [0,0,0,0,0,0,DBgReMatrix[6,0],0],
             [0,0,0,0,0,0,0,DBgReMatrix[7,0]]]);

LMatrix=M-scatterMatrix;
spectrumMatrix=np.matrix(Xg);

fluxMatrix=np.linalg.solve(LMatrix,spectrumMatrix);

#Model Outputs
Keff=np.sum(np.multiply(fissionMatrix,fluxMatrix));
latticeNumber=np.math.ceil(Vcore/Vcell);
fuelLoading=(latticeNumber)*Vfuel*Fuel_density;
PuLoading=fuelLoading*pufraction;
    
print("The Keff is",Keff)
print("The number of fuel elements in the reactor core is",latticeNumber)
print("The total fuel loading is",fuelLoading,"kg" )
print("The Pu-239 loading is",PuLoading,"kg")

#Flux Normalization (assume energy released per fission is 200 MeV)
Ef=200*(1.60218e-13);
Pf=100e+6;
collapseSigF=sum(np.multiply(fluxMatrix,(np.matrix(fissCellg).T)))/sum(fluxMatrix)   
normalFluxVal=((Pf)/(Ef*collapseSigF));
percentFlux=((1/np.sum(fluxMatrix))*fluxMatrix);
percentFlux=percentFlux.T
reactorEnergyFlux=np.multiply(normalFluxVal,percentFlux);
    
#Flux Plots
plt.plot(np.array([[2200,1510,560,205,75,27.5,7.875,0.375]]),np.asarray(reactorEnergyFlux),'ro')  
plt.xlabel("Energy (keV)")
plt.ylabel("Scalar Flux ")
plt.title("Scalar Flux as a Function of Energy")
