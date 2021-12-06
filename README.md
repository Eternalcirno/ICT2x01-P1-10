
<div id="top"></div>
<!-- PROJECT LOGO r-->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">CRUSH GEAR</h3>

  <p align="center">
    ICT2x01-P1-10 Project
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</div>

<!-- How to run-->
## How to Run

### Dependencies
Flask

Python-Dotenv

Python-Decouple

### Installation

```
pip install -r requirements.txt
```

### Execution
Both portal and car need to be connected to the same mobile hotspot
1. Power up the car
2. Run portal.py
4. Car should be connected within 30 seconds
5. Access website: http://127.0.0.1:5000
6. Code and start the car!

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- development workflow -->
## Development Workflow

<!-- UAT -->
## UAT

### Use Case Diagram
<div align='center'>
<img src="images/UCD.png" alt="UCD" height=70% width = 70%>
</div>

### System State Diagram
<div align='center'>
<img src="images/SSD.png" alt="SSD" height=70% width = 70%>
</div>

For the system state diagram, the end screen has been removed and replaced with a landing page that has a tutorial video. The end screen is removed because coding requires a lot of testing, and an end screen is disruptive for the process. Users can instead see their score on the dashboard.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- whitebox testing -->
## Whitebox Testing

### Admin Authentication - Test Case


https://user-images.githubusercontent.com/19475364/144821629-be00601c-c1ff-4526-9c3c-f18b26cd86c6.mp4


The video above shows all the test cases for admin authentication. In total, there are 14 test cases that was being run. We use the built in unit testing framework that python has provided.

The list of test cases includes:
* testEmptyPass
* testEmptyUser
* testBan
* testBadCreds
* testUnBan
* testLogin
* testEmptyNewPass
* testEmptyConfNewPass
* testEmptyOldPass
* testWrongOldPass
* testSamePass
* testDiffPass
* testPol
* testChange

### Coverage Statistic

#### Login

![wbcov (2)](https://user-images.githubusercontent.com/19475364/144804420-6a51f2e1-2ba1-4b37-8d80-46d43793c817.jpg)

Total statement = 16

testUnBan = 3/16

testEmptyUser = 2/16

testEmptyPass = 2/16

testLogin = 3/16

testBadCreds = 3/16

testBan = 3/16

#### Change Password
![wbcov2](https://user-images.githubusercontent.com/19475364/144811949-a1899c8a-6892-4c74-8614-7887815e5655.jpg)

Total statement = 19

testSamePass = 2/19

testEmptyNewPass = 2/19

testEmptyConfNewPass = 2/19

testEmptyOldPass = 2/19

testWrongOldPass = 2/19

testDiffPass = 2/19

testPol =  2/19

testChange = 5/19






## Members

Ng Jing Yong - 2002478@sit.singaporetech.edu.sg

Ng Jing Fang - 2002855@sit.singaporetech.edu.sg

Mohamad Lutfee - 2001369@sit.singaporetech.edu.sg

Seah Yuan Shengh - 2000532@sit.singaporetech.edu.sg

Yang Yuqin - 2002620@sit.singaporetech.edu.sg

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
