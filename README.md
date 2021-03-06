## CS410-Project
### Final Project for CS410 - Address Standardization and Merging

### Project Goal
Address data in CRM (customer relationship management) tools are typically of poor quality (as one of Alan’s previous bosses used to say, salespeople are not the best data managers).  The poor quality makes it challenging and time consuming to report on a customer base, conduct customer segmentation analyses, etc.  Due to this poor quality and lack of controls, databases typically contain tons of duplicate records/addresses, incomplete addresses, and incorrect addresses/information.  Data stewards/analysts are often tasked with manually fixing the poor quality data, an efficient and time-consuming process.

Our project focused on creating a suite of tools to parse, tag, standardize, and compare lists of addresses as an alternative to expensive Master Data Management and similar systems.  The goal is to be able to use our tools to find duplicates within a single list of addresses as well as across 2 separate address lists.  In essence, our tools are designed to help master the address data so that a database doesn't have duplicates/triplicates, etc.

### Pre-Requisites
The various methods within the address_compare project have been built using Python 3.x. In addition, the following Python packages will need to be installed in order to run the various methods:

- python-crfsuite
```
pip install python-crfsuite
```
- editdistance
```
pip install editdistance
```

##### Additional Python Modules
The following python packages are also being used in the various files.  So please make sure they are installed on your local machine as well (they should all be included as part of the standard python build anyways if using Anaconda):
- collections
- itertools
- json
- pandas
- pickle
- pkg_resources
- random
- re
- scipy
- scikit-learn
- sklearn.metrics (should be part of scikit-learn)


### Running our Functions
In order to run our functions, please make sure to use Python 3 and install the pre-requisites listed above.  We have not built out functionality to run the files directly within GitHub so please make sure to download the full folder to your local machine.  The easiest way to understand how the 3 main/aggregate functions work is to run the master_file.ipynb file in a jupyter notebook.  Test files for each of the run_modes have been provided in the data folder and are listed in the variable section of the master_file.ipynb file.

Also note that old_files_for_tech_review_use folder can be ignored.  Those were sandbox files used as part of the technology review.

There are various functions within the reference_data.py file that help with the standardization of the addresses.  However, as the output of these functions are written to JSON files, this file only needs to be re-run if any of the source reference data files (street types, unit types, cities, states, zip codes, etc.) are changed.  Otherwise, this file can be ignored. 

If running the master_file.ipynb and writing the output to excel (there is a variable to control whether the output is printed in the notebook or written to excel), the output files will be found in the output folder.

The 3 functions within the aggregate_functions.py file are wrappers for all of the functions and methods required to perform the address tagging and matching on two separate files containing addresses.  These 3 functions are included in the master_file.ipynb discussed below for ease of testing our project.

### Example Files
The [master_file.ipynb](https://github.com/aberk104/CS410-Project/blob/master/master_file.ipynb) can be run using jupyter notebook.
This file has separate calls to each of the 3 functions in the aggregate_functions.py file (which themselves are self-contained functions to access the address parser, tagger, and matcher).
Variables can be set at the top of the master_file.ipynb to control the different run_modes and choose a different set of input files.
Instructions for how to run the master_file, what each variable means, etc. can be found directly in that file.

The [Train Address Classifier.ipynb](https://github.com/aberk104/CS410-Project/blob/master/Train%20Address%20Classifier.ipynb) as well as the [Matching with the random forest model.ipynb](https://github.com/aberk104/CS410-Project/blob/master/Matching%20with%20the%20random%20forest%20model.ipynb) show how the random forest model for probabilistic matching was trained and validated.  As noted in the Future Enhancements section, although the random forest model performed well with the training data, it performed poorly with the test/real data.  Further refinements will be needed to optimize the probabilistic matching.

The [Train CRF Model.ipynb](https://github.com/aberk104/CS410-Project/blob/master/Train%20CRF%20Model.ipynb) file walks through how the CRF model was trained in order to tag the address components.

### Documentation
Additional documentation for the recommended functions to be used can be found on [Read the Docs](http://cs410-project-address-tagging-and-matching.readthedocs.io/en/latest/).
The 3 functions within the aggregate_functions.py file and the main address_randomizer function in the address_randomizer.py file are listed on the site.  The site also includes the doc-strings for the AddressTagger class and the exact matcher function.
As the remaining functions can be accessed directly from the aggregate_functions.py file, doc strings have been included directly in those files but have not been shared on the site at this time.

### Presentations
A powerpoint deck describing the different steps of our project, how the tagger works, and the performance can be found by clicking on this [link](https://docs.google.com/presentation/d/1j0d68tpCN3YOiGgo-3gNN9E-0Qbb-jnMm7UCqk6gkLU/edit?usp=sharing).

A voiced presentation (voice-over of the powerpoint deck including a demo of the various functions/modules) can be found by clicking on this [link](https://drive.google.com/file/d/1ZXeZ6jLGoNvRAFzYxuJWbp89l_2fIv5B/view?usp=sharing).

### Contributors
This project was completed by Alan Berk and Colin Fraser as part of CS-410 through UIUC.  
For our UIUC instructors, we distributed the work as follows:
- Colin focused on:
  - The Address Tagger itself. Creating the training data using Amazon MTurk, training the CRF model, and testing with different feature sets to optimize the tagger.
  - The Probabilistic Matcher. Creating the training data, training the model utilizing Random Forest, and testing with different feature sets to optimize the matcher.
  - The powerpoint presentation as well as the voice-over/demo.
  - Sourcing of the Colorado Stores and Washington State Marijuana Applicants test files.
- Alan focused on:
  - The various functions used to standardize the addresses within the standardizers.py file, the random_addresses function in the address_randomizer, and the creation of the nested reference data dictionaries via the reference_data.py file.
  - The exact_match logic, the creation of the aggregated functions in aggregate_functions.py, and the parameterized example in the master_file.ipynb.
  - Tagging the various test files (Colorado Stores, Washington State Marijuana Applicants, and the tagged/standardized Washington State file) to be able to test the Address Tagger and Matcher functions via the master_file.ipynb.  Testing the various functions and providing feedback to Colin in order to further optimize the models.
  - The documentation on *Read the Docs* as well as the readme file
- There was constant communication between Alan and Colin to discuss different approaches for the parsing, tagging, standardization, matching, etc. We were constantly collaborating during the development and testing phases to ensure all functions were optimized and the project output was as good as possible.  We focused on different parts of the project but it was a group effort to complete it.

### Potential Enhancements/Next Steps
The following is a list of potential improvements/enhancements that can be made to further improve the program:
- Due to its complexity, we tagged items like Highway 17 or County Road 585 with Highway/County Road as STREET_TYPE and 17/585 as STREET_NAME.  However, the USPS defines items like that to all be the STREET_NAME with nothing as the STREET_TYPE.  The additional complexity also lies in the fact that there are examples like Ute Highway where Highway is supposed to be tagged as the STREET_TYPE.  Therefore, a future enhancement would be re-train the CRF model (and include new features) or find an alternative model to be able to change how Highway/County Road/etc. are tagged.
- Additional improvements can potentially be made to the Address Tagger in terms of the number of features being used.  I.e., potentially adding features to capture Interstate or other things may further improve the Tagger performance.
- The address tagger also experiences some issues if the street address contains 2 or more street type words (e.g., Elm Street Drive). Further training and enhancements will be needed to address this.
- The probabilistic matcher was the last item worked on as an attempted add-on to the program.  We have experienced some issues optimizing the probabilistic matcher and ensuring that it is working correctly with the real address data (working well with the training data).  We are currently seeing issues in scoring the matches correctly so we don't recommend that this be used at this time.  More work/enhancements are needed in order to finalize/optimize the probabilistic matcher.
- Work was started to do some pre-processing on the Zip Codes before passing them into the probabilistic matcher.  The code was commented out but the goal would be to match on Zip Codes before passing the address lists to the probabilistic matcher (so that only items that are in the same Zip Code are attempted to be matched).
- All of the functions/methods exist to de-dupe a single address list. It can be compared against itself by having both file inputs to the tag and compare function be the same file.  But an obvious next step would be to create a simple method to just parse, tag, standardize, and de-dupe a single file in a more straightforward manner.
- As the focus of the address tagger was on the street addresses, state names are not being standardized at this point in time. For this iteration, state names are assumed to be the 2 character USPS abbreviations.