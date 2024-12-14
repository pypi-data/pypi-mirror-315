# pramanpatram-lib

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyPi](https://img.shields.io/badge/pypi-%23ececec.svg?style=for-the-badge&logo=pypi&logoColor=1f73b7)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)

Python Wrapper Library for Pramanpatram to generate event certificates

## Supported Features
- Generating event certificates with only attendee names

## Installation

```sh
$ pip install pramanpatram
```

## Getting Started

Import the package

```py
import Pramanpatram
```
Create `.csv` file containing the Column header as `Attendees` with the Attendee names

Pass the parameters into `patram.generate_certificates()`:


<table>
  <tr>
    <th>Parameter</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>csv_path</code></td>
    <td>Path of CSV File</td>
  </tr>
    <tr>
    <td><code>sample_path</code></td>
    <td>Path of Certificate Template File</td>
  </tr>
    <tr>
    <td><code>text_coords_x</code></td>
    <td> X Coordinate of the text to be printed</td>
  </tr>
  <tr>
    <td><code>text_coords_y</code></td>
    <td> Y Coordinate of the text to be printed</td>
  </tr>
  <tr>
    <td><code>text_size</code></td>
    <td>Size of text to be printed</td>
  </tr>
  <tr>
    <td><code>r_Value</code></td>
    <td>Red Colour Value (Set to 0 for Black)</td>
  </tr>
  <tr>
    <td><code>g_Value</code></td>
    <td>Green Colour Value (Set to 0 for Black)</td>
  </tr>
  <tr>
    <td><code>b_Value</code></td>
    <td>Blue Colour Value (Set to 0 for Black)</td>
  </tr>
  <tr>
    <td><code>text_width</code></td>
    <td>Width of text</td>
  </tr>
  <tr>
    <td><code>certificate_text</code></td>
    <td>Text to be printed on the certificate (use {name} to print the name in the position)</td>
  </tr>
  <tr>
    <td><code>certificate_path</code></td>
    <td>Location to save certificates</td>
  </tr>
</table>

Run the program to find your certificates in the path you mentioned.

## Documentation

### Available Methods
- `generate_certificates(self, csv_path, sample_path, text_coords_x, text_coords_y, text_size, r_value, g_value, b_value, text_width, certificate_text, certificate_path)`

  Takes 12 inputs and generates the certificates in the specified path

  Example:

  ```py
  import os
  from pramanpatram.pramanpatram import Pramanpatram

  def test_generate_certificate():
      csv_path = "attendees.csv"
      sample_path = "sample.jpg"
      text_coords_x = 110
      text_coords_y = 120
      text_size = 20
      r_value = 0
      g_value = 0
      b_value = 0
      text_width = 40
      certificate_text = "Thanks {name}"
      certificate_path = "certificates"

      if not os.path.exists(csv_path):
          print(f"CSV file not found at path: {csv_path}")
          return

      if not os.path.exists(certificate_path):
         os.makedirs(certificate_path)
         print(f"Created directory for certificates at path: {certificate_path}")

      patram = Pramanpatram()
      result = patram.generate_certificates(csv_path, sample_path, text_coords_x, text_coords_y, text_size, r_value, g_value, b_value, text_width, certificate_text,       certificate_path)
      print(result)

  test_generate_certificate()
  ```
