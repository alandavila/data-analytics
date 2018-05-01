# import dependencies
import pandas as pd

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
otu  = Base.classes.otu
samples  = Base.classes.samples
samples_metadata  = Base.classes.samples_metadata

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    """Return the dashboard homepage."""
    return render_template("index.html")

@app.route('/names')
def sample_names():
    """List of sample names.

    Returns a list of sample names in the format
    [
        "BB_940",
        "BB_941",
        "BB_943",
        "BB_944",
        "BB_945",
        "BB_946",
        "BB_947",
        ...
    ]

    """
    results = session.query(samples_metadata.SAMPLEID).all()
    results = ['BB_' + str(id[0]) for id in results]

    return jsonify(results)

@app.route('/otu')
def otu_description():
    """List of OTU descriptions.

    Returns a list of OTU descriptions in the following format

    [
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Bacteria",
        "Bacteria",
        "Bacteria",
        ...
    ]
    """
    results = session.query(otu.lowest_taxonomic_unit_found).all()
    results = [str(result[0]) for result in results]
    return jsonify(results)

@app.route('/metadata/<sample>')
def get_sample(sample):
    """MetaData for a given sample.

    Args: Sample in the format: `BB_940`

    Returns a json dictionary of sample metadata in the format

    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """
    query = [
        samples_metadata.AGE,
        samples_metadata.BBTYPE,
        samples_metadata.ETHNICITY,
        samples_metadata.GENDER,
        samples_metadata.LOCATION,
        samples_metadata.SAMPLEID
    ]
    id = sample[3:]
    results = session.query(*query).filter(samples_metadata.SAMPLEID == id).all()
    results = results[0]
    result = {}
    result['AGE'] = results[0]
    result['BBTYPE'] = results[1]
    result['ETHNICITY'] = results[2]
    result['GENDER'] = results[3]
    result['LOCATION'] = results[4]
    result['SAMPLEID'] = results[5]

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
