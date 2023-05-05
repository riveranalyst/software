


User's Manual
- Install pandoc, I used conda for it (conda install -c conda-forge pandoc)
- Convert README.md to PDF:

	pandoc -V geometry:margin=1in -o output.pdf input.md