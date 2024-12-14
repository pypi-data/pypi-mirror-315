"""Application route handlers."""

import logging
from io import BytesIO
from typing import Dict
from urllib import parse

import cachetools
from flasgger import swag_from
from flask import request
from werkzeug.datastructures import FileStorage

from validata_api.api import app, config
from validata_api.api.json_errors import (
    abort_json,
    abort_with_operation_error,
    make_json_response,
)
from validata_core import fetch_remote_schema
from validata_core import resource_service as resource
from validata_core import validation_service
from validata_core.domain.types import (
    ErrType,
    SchemaDescriptor,
    TypedException,
    ValidataResource,
)

# Schema cache size (nb of simultaneously stored schemas)
SCHEMA_CACHE_SIZE = 20
# Schema time to live (in seconds)
SCHEMA_CACHE_TTL = 60


log = logging.getLogger(__name__)


def bytes_data(f: FileStorage) -> bytes:
    """Get bytes data from Werkzeug FileStorage instance."""
    iob = BytesIO()
    f.save(iob)
    iob.seek(0)
    return iob.getvalue()


@app.route("/")
def index():
    """Home."""
    apidocs_href = "{}/apidocs".format(config.SCRIPT_NAME)
    apidocs_url = parse.urljoin(request.url, apidocs_href)
    return make_json_response(
        {
            "apidocs_href": apidocs_href,
            "message": (
                "This is the home page of Validata Web API. "
                f"Its documentation is here: {apidocs_url}"
            ),
        },
        args=None,
    )


BASE_URL = "https://gitlab.com/opendatafrance/scdl/deliberations"

SPECS_DICT = {
    "get": {
        "summary": "Validate a tabular file from its URL",
        "parameters": [
            {
                "name": "schema",
                "in": "query",
                "type": "string",
                "format": "url",
                "description": "URL of schema to use for validation",
                "example": f"{BASE_URL}/raw/master/schema.json",
                "required": True,
            },
            {
                "name": "url",
                "in": "query",
                "type": "string",
                "format": "url",
                "description": "URL of tabular file to validate",
                "example": f"{BASE_URL}/raw/v2.0/examples/Deliberations_ok.csv",
                "required": True,
            },
            {
                "name": "ignore_header_case",
                "in": "query",
                "type": "boolean",
                "description": "Should validation of headers be case-insensitive?",
                "default": "false",
                "required": False,
            },
        ],
        "produces": ["application/json"],
    },
    "post": {
        "summary": "Validate an uploaded tabular file",
        "parameters": [
            {
                "name": "schema",
                "in": "formData",
                "type": "string",
                "format": "url",
                "description": "URL of schema to use for validation",
                "example": f"{BASE_URL}/raw/master/schema.json",
                "required": True,
            },
            {
                "name": "file",
                "in": "formData",
                "type": "file",
                "description": "The file to upload",
                "required": True,
            },
            {
                "name": "ignore_header_case",
                "in": "formData",
                "type": "boolean",
                "description": "Should the validation of headers be case-insensitive?",
                "default": "false",
                "required": False,
            },
        ],
        "consumes": ["multipart/form-data"],
        "produces": ["application/json"],
    },
    "definitions": {
        "ValidationResponse": {
            "type": "object",
            "properties": {
                "schema": {"type": "string"},
                "url": {"type": "string", "format": "uri", "pattern": "^https?://"},
                "options": {"$ref": "#/definitions/Options"},
                "report": {"$ref": "#/definitions/Report"},
                "version": {"type": "string"},
                "date": {"type": "string"},
            },
            "required": [
                "schema",
                "url",
                "options",
                "version",
                "date",
                "report",
            ],
        },
        "Options": {
            "type": "object",
            "properties": {"ignore_header_case": {"type": "boolean"}},
        },
        "Report": {
            "type": "object",
            "properties": {
                "valid": {"type": "boolean"},
                "stats": {"$ref": "#/definitions/Stats"},
                "warnings": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/ValidationError"},
                },
                "errors": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/ValidationError"},
                },
            },
        },
        "ValidationError": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "type": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "rowNumber": {"type": "integer"},
                "fieldName": {"type": "string"},
                "fieldNumber": {"type": "integer"},
                "cell": {},
            },
            "required": ["message", "type", "tags"],
        },
        "Stats": {
            "type": "object",
            "properties": {
                "errors": {"type": "integer"},
                "warnings": {"type": "integer"},
                "seconds": {"type": "number"},
                "fields": {"type": "integer"},
                "rows": {"type": "integer"},
                "rows_processed": {"type": "integer"},
            },
            "required": [
                "errors",
                "warnings",
                "seconds",
                "fields",
                "rows",
                "rows_processed",
            ],
        },
    },
    "responses": {
        "200": {
            "description": "Validation report",
            "schema": {"$ref": "#/definitions/ValidationResponse"},
            "examples": [
                {
                    "schema": {},
                    "url": "",
                    "options": {"ignore_header_case": "true"},
                    "report": {
                        "date": "",
                        "valid": "false",
                        "stats": {
                            "errors": 1,
                            "warnings": 0,
                            "seconds": 0.034,
                            "fields": 17,
                            "rows": 1,
                        },
                        "warnings": [],
                        "errors": [
                            {
                                "title": "Comparaison de colonnes",
                                "message": "La valeur de la colonne PREF_DATE `2017-02-03` devrait être supérieure ou égale à la valeur de la colonne DELIB_DATE `2017-10-15`..",
                                "type": "compare-columns-value",
                                "cell": "2017-02-03",
                                "fieldName": "PREF_DATE",
                                "rowNumber": 2,
                                "fieldNumber": 11,
                                "tags": ["#body"],
                            }
                        ],
                    },
                    "validata-table-version": "0.11.1",
                }
            ],
        },
        "400": {
            "description": "Error, no validation could be preformed",
            "schema": {
                "type": "object",
                "properties": {
                    "schema": {"type": "string"},
                    "url": {"type": "string", "format": "uri", "pattern": "^https?://"},
                    "error": {
                        "type": "object",
                        "properties": {
                            "message": {"type": "string"},
                            "type": {"type": "string"},
                        },
                    },
                },
                "required": ["schema", "url", "error", "options"],
            },
            "examples": [{"message": "Unsupported format error"}],
        },
    },
}


@cachetools.cached(cachetools.TTLCache(SCHEMA_CACHE_SIZE, SCHEMA_CACHE_TTL))
def download_schema(schema_url: str) -> SchemaDescriptor:
    """Download schema by its given url.

    Raises:
      TypedException
    """
    return fetch_remote_schema(schema_url)


def get_args(request) -> Dict[str, str]:
    if request.method == "GET":
        args = {
            "schema": request.args.get("schema"),
            "url": request.args.get("url"),
            "ignore_header_case": request.args.get("ignore_header_case"),
        }
    else:
        assert request.method == "POST", request.method
        args = {
            "schema": request.form.get("schema"),
            "ignore_header_case": request.form.get("ignore_header_case"),
        }
    return args


def create_validata_resource(
    args: Dict[str, str],
) -> ValidataResource:
    validata_resource = None

    if request.method == "GET":
        # URL validation
        if not args["url"]:
            err = TypedException(
                'Missing or empty "url" parameter', ErrType.SOURCE_ERROR
            )
            abort_with_operation_error(err, 400, args)

        try:
            validata_resource = resource.from_remote_file(args["url"])
        except TypedException as err:
            abort_with_operation_error(err, 400, args)
        except Exception as e:
            abort_json(500, args, f"Unknown error: { e }")

    elif request.method == "POST":
        # Uploaded file validation
        f = request.files.get("file")

        if f is None:
            err = TypedException(
                'Missing or empty "file" parameter', ErrType.SOURCE_ERROR
            )
            abort_with_operation_error(err, 400, args)

        filename = f.filename if f.filename else ""

        try:
            validata_resource = resource.from_file_content(filename, bytes_data(f))
        except TypedException as err:
            abort_with_operation_error(err, 400, args)

    else:
        abort_json(405, args, "Request method not allowed")

    return validata_resource


@app.route("/validate", methods={"GET", "POST"})
@swag_from(SPECS_DICT)
def validate():
    """Validate endpoint."""

    args = get_args(request)

    if not args["schema"]:
        err = TypedException(
            'Missing or empty "schema" parameter', ErrType.SOURCE_ERROR
        )
        abort_with_operation_error(err, 400, args)

    # Download Schema from URL to get control on cache
    # schema json dict is passed to validate function as a dict
    try:
        schema_dict = download_schema(args["schema"])
    except TypedException as err:
        abort_with_operation_error(err, 400, args)

    try:
        validata_resource = create_validata_resource(args)
    except TypedException as err:
        body = {"error": {"message": str(err), "type": err.type}}
        return make_json_response(body, args)

    if args["ignore_header_case"] is None:
        ignore_header_case = False
    else:
        ignore_header_case = args["ignore_header_case"].lower() == "true"

    validation_report = validation_service.validate_resource(
        validata_resource, schema_dict, ignore_header_case
    )

    formatted_validation_report = validation_report.format()

    return make_json_response(formatted_validation_report, args)
