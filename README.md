# refills_marker_generator
A collection of nodes to generate QRmarkers used in the REFILLS project.

## Printable markers with Chilitags inside
This package contains a script that allows you to create printable markers with Chilitags markers inside. The resulting markers will look like this:

<img src="https://raw.githubusercontent.com/refills-project/refills_marker_generator/master/doc/17.svg.png" width="200"> <img src="https://raw.githubusercontent.com/refills-project/refills_marker_generator/master/doc/18.svg.png" width="200">

### Rationale

The printable markers also contain some human-readable information that indicate:
- which number the Chilitag marker encodes
- on which side of a shelf this marker should be attached

To ease visual inspection, the human-readable information is printed in different colors. As a result, it should be trivial to infer --even from a distance-- whether a set of markers is correctly placed on a shelf. Also, the colors have been chosen to be distinguishable by person with colorblindness.

### Installation 
TODO

### Usage
To create a single marker file encoding ```<NUM>``` call:
 
```shell
$ rosrun refills_marker_generator gen_chilitags <NUM>
```

To create several marker files, starting with ```<START>``` and ending with ```<END>```, call:
  
```shell
$ rosrun refills_marker_generator gen_chilitags <START> <END>
```

Note, all generated markers (and generated intermediate files) will be placed inside your current directory.

The script comes with has a short help output:
```shell
$ rosrun refills_marker_generator gen_chilitags -h
usage: gen_chilitags [-h] first [last]

Create some augmented 'Chilitag' QR markers for printing.

positional arguments:
  first       The first number to encode. It has to be between 1 and 1023.
  last        The last number to encode. It has to be between 1 and 1023,and
              it has to be also greater than 'first'.

optional arguments:
  -h, --help  show this help message and exit
```
