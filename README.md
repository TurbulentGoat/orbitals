# Interactive orbitals tool

1) Download the code/copy to whatever you write your code in.
2) Install/update streamlit:
   (If on Linux: "sudo pip install streamlit --break-system-packages" .. or preferrably use a virtual environment!)
3) Run the program with:
   ("streamlit run orbitals.py")

If you notice any errors, please let me know.

---

To understand how electrons fill atomic orbitals, follow these steps:

1. **Start with the lowest energy orbital**:
   - **n=1, l=0, m=0**: This corresponds to the **1s orbital**. It is the first orbital to be filled and has a spherical shape.

2. **Move to the next energy level**:
   - **n=2, l=0, m=0**: This corresponds to the **2s orbital**. It is the next orbital to be filled and also has a spherical shape but is larger than the 1s orbital.

3. **Fill the 2p orbitals**:
   - **n=2, l=1, m=-1**: This corresponds to the **2p orbital** oriented along the negative y-axis.
   - **n=2, l=1, m=0**: This corresponds to the **2p orbital** oriented along the z-axis.
   - **n=2, l=1, m=1**: This corresponds to the **2p orbital** oriented along the positive y-axis.

4. **Proceed to the 3s orbital**:
   - **n=3, l=0, m=0**: This corresponds to the **3s orbital**. It is the next orbital to be filled and has a spherical shape but is larger than the 2s orbital.

5. **Fill the 3p orbitals**:
   - **n=3, l=1, m=-1**: This corresponds to the **3p orbital** oriented along the negative y-axis.
   - **n=3, l=1, m=0**: This corresponds to the **3p orbital** oriented along the z-axis.
   - **n=3, l=1, m=1**: This corresponds to the **3p orbital** oriented along the positive y-axis.

6. **Fill the 4s orbital before the 3d orbitals** (according to the Aufbau principle):
   - **n=4, l=0, m=0**: This corresponds to the **4s orbital**. It is the next orbital to be filled and has a spherical shape but is larger than the 3s orbital.

7. **Fill the 3d orbitals**:
   - **n=3, l=2, m=-2**: This corresponds to the **3d orbital** with a complex shape.
   - **n=3, l=2, m=-1**: This corresponds to the **3d orbital** with a different orientation.
   - **n=3, l=2, m=0**: This corresponds to the **3d orbital** oriented along the z-axis.
   - **n=3, l=2, m=1**: This corresponds to the **3d orbital** with another orientation.
   - **n=3, l=2, m=2**: This corresponds to the **3d orbital** with yet another orientation.

8. **Continue with the 4p orbitals**:
   - **n=4, l=1, m=-1**: This corresponds to the **4p orbital** oriented along the negative y-axis.
   - **n=4, l=1, m=0**: This corresponds to the **4p orbital** oriented along the z-axis.
   - **n=4, l=1, m=1**: This corresponds to the **4p orbital** oriented along the positive y-axis.

By following these steps, you can visualize the order in which electrons fill the atomic orbitals according to the Aufbau principle. Each set of quantum numbers (n, l, m) corresponds to a specific orbital with a unique shape and orientation.
