# Orbital API DevNet Context

Source URL: https://developer.cisco.com/docs/orbital/introduction/#orbital-api

Source title: Orbital API - Cisco DevNet

Retrieved: 2026-06-02

Import type: Structured project context and link index from Cisco DevNet Orbital API documentation. This file is not a verbatim copy of the page.

## Summary

The Orbital API is a RESTful API for programmatically managing Orbital queries and scripts and retrieving query and script output.

The API supports automation and integrations around Orbital's endpoint visibility and response capabilities.

Key API use cases from the page:

- Schedule queries or scripts.
- Retrieve query or script results.
- Use catalog queries and scripts.
- Manage remote data store destinations for scheduled results.
- Build custom integrations around Orbital investigation and response workflows.

## Product Context From API Page

Orbital is described as a cloud-based attack research and response tool. It lets security teams gather system and security information from network-connected endpoints and respond to threats.

Orbital query work uses SQL through osquery. Orbital response work uses Python scripts.

Supported platforms listed on the API introduction page include Windows client/server versions, macOS versions, and several Linux distributions.

## API Servers

The API reference payload identifies regional server URLs:

- North America: `https://enterprise.orbital.amp.cisco.com/v0`
- Asia, Pacific, Japan, and China: `https://apjc.orbital.amp.cisco.com/v0`
- Europe: `https://eu.orbital.amp.cisco.com/v0`

Runtime note from catalog import on 2026-06-02:

- `https://enterprise.orbital.amp.cisco.com/v0` did not resolve in local DNS during testing.
- `https://orbital.amp.cisco.com/v0` resolved and successfully returned HTTP 200 for the North America catalog endpoints.

## Authentication Context

The API reference uses an authorization header API key scheme.

Observed authentication pattern:

- Header name: `authorization`
- Value format: `Bearer <token>`

The DevNet page references SecureX token generation for authentication. Exact token generation steps should be verified on the Cisco authentication page before implementation.

## API Categories

The page links API operations and models in these major areas:

- Guides: introduction, authentication, getting started, queries, script, results, webhooks, changelog, overview.
- Query operations: organization catalog queries, query creation, disabling, and live query execution.
- Script operations: stock scripts, organization catalog scripts, scheduled scripts, live script execution, script jobs, and script results.
- Misc operations: downloads, feature IDs, feature updates, and service status.
- Jobs/results operations: job status and query result retrieval.
- Stock catalog operations: public stock query catalog.
- Webhook operations: create, fetch, update, delete, ping, jobs, and sending existing results.
- Model/schema pages: request and response schemas for queries, scripts, results, webhooks, errors, jobs, and related objects.

## Operation Link Index

### Query Operations

- Fetch All Organization Catalog Queries: https://developer.cisco.com/docs/orbital/fetch-all-organization-catalog-queries
- Create an Organization Catalog Query: https://developer.cisco.com/docs/orbital/create-an-organization-catalog-query
- Update an Organization Catalog Query: https://developer.cisco.com/docs/orbital/update-an-organization-catalog-query
- Disable an Organization Catalog Query: https://developer.cisco.com/docs/orbital/disable-an-organization-catalog-query
- Fetch an Organization Catalog Query: https://developer.cisco.com/docs/orbital/fetch-an-organization-catalog-query
- Create Query: https://developer.cisco.com/docs/orbital/create-query
- Disables a query: https://developer.cisco.com/docs/orbital/disables-a-query
- Create Live Query: https://developer.cisco.com/docs/orbital/create-live-query

### Script Operations

- Fetch All Catalog Stock Scripts: https://developer.cisco.com/docs/orbital/fetch-all-catalog-stock-scripts
- Fetch All Organization Catalog Scripts: https://developer.cisco.com/docs/orbital/fetch-all-organization-catalog-scripts
- Create an Organization Catalog Script: https://developer.cisco.com/docs/orbital/create-an-organization-catalog-script
- Disable an Organization Catalog Script: https://developer.cisco.com/docs/orbital/disable-an-organization-catalog-script
- Fetch an Organization Catalog Script: https://developer.cisco.com/docs/orbital/fetch-an-organization-catalog-script
- Update an Organization Catalog Script: https://developer.cisco.com/docs/orbital/update-an-organization-catalog-script
- Schedule Execution of a Script: https://developer.cisco.com/docs/orbital/schedule-execution-of-a-script
- Delete a Script Job: https://developer.cisco.com/docs/orbital/delete-a-script-job
- Fetch Script Job Info: https://developer.cisco.com/docs/orbital/fetch-script-job-info
- Rename a Script Job: https://developer.cisco.com/docs/orbital/rename-a-script-job
- Fetch Script Job Results: https://developer.cisco.com/docs/orbital/fetch-script-job-results
- Live Execution of a Script: https://developer.cisco.com/docs/orbital/live-execution-of-a-script

### Misc, Jobs, Stock, And Webhook Operations

- Create a download request: https://developer.cisco.com/docs/orbital/create-a-download-request
- Fetch an available download: https://developer.cisco.com/docs/orbital/fetch-an-available-download
- List available downloads: https://developer.cisco.com/docs/orbital/list-available-downloads
- Id Of Features: https://developer.cisco.com/docs/orbital/id-of-features
- Id Of Feature Fetch: https://developer.cisco.com/docs/orbital/id-of-feature-fetch
- Update orbital feature: https://developer.cisco.com/docs/orbital/update-orbital-feature
- Check service status: https://developer.cisco.com/docs/orbital/check-service-status
- Get status information about a job: https://developer.cisco.com/docs/orbital/get-status-information-about-a-job
- Returns results of a particular query: https://developer.cisco.com/docs/orbital/returns-results-of-a-particular-query
- Returns the public stock query catalogue: https://developer.cisco.com/docs/orbital/returns-the-public-stock-query-catalogue
- Fetch the collection of webhooks: https://developer.cisco.com/docs/orbital/fetch-the-collection-of-webhooks
- Create a new webhook: https://developer.cisco.com/docs/orbital/create-a-new-webhook
- Delete an existing webhook: https://developer.cisco.com/docs/orbital/delete-an-existing-webhook
- Fetch the webhook for a specific id: https://developer.cisco.com/docs/orbital/fetch-the-webhook-for-a-specific-id
- Update existing webhook: https://developer.cisco.com/docs/orbital/update-existing-webhook
- Fetch the jobs associated with a particular webhook: https://developer.cisco.com/docs/orbital/fetch-the-jobs-associated-with-a-particular-webhook
- Sends a ping to an existing webhook: https://developer.cisco.com/docs/orbital/sends-a-ping-to-an-existing-webhook
- Sends an existing result to an existing webhook: https://developer.cisco.com/docs/orbital/sends-an-existing-result-to-an-existing-webhook

## Guide Link Index

- Orbital API / Introduction: https://developer.cisco.com/docs/orbital/introduction
- Authentication: https://developer.cisco.com/docs/orbital/authentication
- Getting Started: https://developer.cisco.com/docs/orbital/getting-started
- Queries: https://developer.cisco.com/docs/orbital/queries
- Script: https://developer.cisco.com/docs/orbital/script
- Results: https://developer.cisco.com/docs/orbital/results
- Webhooks: https://developer.cisco.com/docs/orbital/webhooks
- API Changelog: https://developer.cisco.com/docs/orbital/api-changelog
- API Reference / Overview: https://developer.cisco.com/docs/orbital/overview

## Model And Schema Link Index

- AllowOSArray: https://developer.cisco.com/docs/orbital/allowosarray
- Args: https://developer.cisco.com/docs/orbital/args
- AuthorInfo: https://developer.cisco.com/docs/orbital/authorinfo
- CatalogQueriesResponse: https://developer.cisco.com/docs/orbital/catalogqueriesresponse
- CatalogQueryResponse: https://developer.cisco.com/docs/orbital/catalogqueryresponse
- CatalogScript: https://developer.cisco.com/docs/orbital/catalogscript
- CatalogScriptArgs: https://developer.cisco.com/docs/orbital/catalogscriptargs
- CatalogScriptRequest: https://developer.cisco.com/docs/orbital/catalogscriptrequest
- CatalogScriptResponse: https://developer.cisco.com/docs/orbital/catalogscriptresponse
- CatalogScriptsResponse: https://developer.cisco.com/docs/orbital/catalogscriptsresponse
- CategoryInfo: https://developer.cisco.com/docs/orbital/categoryinfo
- Config: https://developer.cisco.com/docs/orbital/config
- En: https://developer.cisco.com/docs/orbital/en
- EndpointsOptions: https://developer.cisco.com/docs/orbital/endpointsoptions
- ErrorInfo: https://developer.cisco.com/docs/orbital/errorinfo
- ErrorMsg: https://developer.cisco.com/docs/orbital/errormsg
- ErrorMsg400CatalogQueryDelete: https://developer.cisco.com/docs/orbital/errormsg400catalogquerydelete
- ErrorMsg400CatalogQueryGet: https://developer.cisco.com/docs/orbital/errormsg400catalogqueryget
- ErrorMsg400CatalogQueryPostLarge: https://developer.cisco.com/docs/orbital/errormsg400catalogquerypostlarge
- ErrorMsg400CatalogQueryPut: https://developer.cisco.com/docs/orbital/errormsg400catalogqueryput
- ErrorMsg400CatalogScriptDelete: https://developer.cisco.com/docs/orbital/errormsg400catalogscriptdelete
- ErrorMsg400CatalogScriptGet: https://developer.cisco.com/docs/orbital/errormsg400catalogscriptget
- ErrorMsg400CatalogScriptPostLarge: https://developer.cisco.com/docs/orbital/errormsg400catalogscriptpostlarge
- ErrorMsg400CatalogScriptPut: https://developer.cisco.com/docs/orbital/errormsg400catalogscriptput
- ErrorMsg400DownloadFetch: https://developer.cisco.com/docs/orbital/errormsg400downloadfetch
- ErrorMsg400LiveQuery: https://developer.cisco.com/docs/orbital/errormsg400livequery
- ErrorMsg400LiveScriptPost: https://developer.cisco.com/docs/orbital/errormsg400livescriptpost
- ErrorMsg400Query: https://developer.cisco.com/docs/orbital/errormsg400query
- ErrorMsg400ScheduleScriptPost: https://developer.cisco.com/docs/orbital/errormsg400schedulescriptpost
- ErrorMsg400ScriptJobDelete: https://developer.cisco.com/docs/orbital/errormsg400scriptjobdelete
- ErrorMsg400ScriptJobGet: https://developer.cisco.com/docs/orbital/errormsg400scriptjobget
- ErrorMsg400ScriptJobGetResult: https://developer.cisco.com/docs/orbital/errormsg400scriptjobgetresult
- ErrorMsg400ScriptJobPatch: https://developer.cisco.com/docs/orbital/errormsg400scriptjobpatch
- ErrorMsg401MissingToken: https://developer.cisco.com/docs/orbital/errormsg401missingtoken
- ErrorMsg403AuthInvalid: https://developer.cisco.com/docs/orbital/errormsg403authinvalid
- ErrorMsg403FeatureUpdate: https://developer.cisco.com/docs/orbital/errormsg403featureupdate
- ErrorMsg403Forbidden: https://developer.cisco.com/docs/orbital/errormsg403forbidden
- ErrorMsg404DownloadFetch: https://developer.cisco.com/docs/orbital/errormsg404downloadfetch
- ErrorMsg404FeatureFetch: https://developer.cisco.com/docs/orbital/errormsg404featurefetch
- ErrorMsg404JobNotFound: https://developer.cisco.com/docs/orbital/errormsg404jobnotfound
- ErrorMsg404WebhookNotFound: https://developer.cisco.com/docs/orbital/errormsg404webhooknotfound
- ErrorMsg500FeatureUpdate: https://developer.cisco.com/docs/orbital/errormsg500featureupdate
- ErrorMsg500InternalServerError: https://developer.cisco.com/docs/orbital/errormsg500internalservererror
- Feature: https://developer.cisco.com/docs/orbital/feature
- FeatureInput: https://developer.cisco.com/docs/orbital/featureinput
- FeaturesResponse: https://developer.cisco.com/docs/orbital/featuresresponse
- HostInfo: https://developer.cisco.com/docs/orbital/hostinfo
- Interface: https://developer.cisco.com/docs/orbital/interface
- Job: https://developer.cisco.com/docs/orbital/job
- JobResultsFormat: https://developer.cisco.com/docs/orbital/jobresultsformat
- LiveQueryOutput: https://developer.cisco.com/docs/orbital/livequeryoutput
- LiveQueryOutputResponse: https://developer.cisco.com/docs/orbital/livequeryoutputresponse
- LiveQueryRequest: https://developer.cisco.com/docs/orbital/livequeryrequest
- LiveScriptOutput: https://developer.cisco.com/docs/orbital/livescriptoutput
- LiveScriptOutputResponse: https://developer.cisco.com/docs/orbital/livescriptoutputresponse
- LiveScriptRequest: https://developer.cisco.com/docs/orbital/livescriptrequest
- LoginInfo: https://developer.cisco.com/docs/orbital/logininfo
- Nodes: https://developer.cisco.com/docs/orbital/nodes
- ObservableInfo: https://developer.cisco.com/docs/orbital/observableinfo
- OKResponse: https://developer.cisco.com/docs/orbital/okresponse
- Options: https://developer.cisco.com/docs/orbital/options
- OSArray: https://developer.cisco.com/docs/orbital/osarray
- OSInfo: https://developer.cisco.com/docs/orbital/osinfo
- OSQueries: https://developer.cisco.com/docs/orbital/osqueries
- OSQuery: https://developer.cisco.com/docs/orbital/osquery
- OSResult: https://developer.cisco.com/docs/orbital/osresult
- ParameterInfo: https://developer.cisco.com/docs/orbital/parameterinfo
- Postback: https://developer.cisco.com/docs/orbital/postback
- Postbacks: https://developer.cisco.com/docs/orbital/postbacks
- PostRequest: https://developer.cisco.com/docs/orbital/postrequest
- Public: https://developer.cisco.com/docs/orbital/public
- Query: https://developer.cisco.com/docs/orbital/query
- QueryCondition: https://developer.cisco.com/docs/orbital/querycondition
- QueryExample: https://developer.cisco.com/docs/orbital/queryexample
- QueryInfo: https://developer.cisco.com/docs/orbital/queryinfo
- QueryRequest: https://developer.cisco.com/docs/orbital/queryrequest
- QueryResult: https://developer.cisco.com/docs/orbital/queryresult
- QueryResultRow: https://developer.cisco.com/docs/orbital/queryresultrow
- ResultsOptions: https://developer.cisco.com/docs/orbital/resultsoptions
- Script: https://developer.cisco.com/docs/orbital/model-script
- ScriptArg: https://developer.cisco.com/docs/orbital/scriptarg
- ScriptArgs: https://developer.cisco.com/docs/orbital/scriptargs
- ScriptConfig: https://developer.cisco.com/docs/orbital/scriptconfig
- ScriptInfo: https://developer.cisco.com/docs/orbital/scriptinfo
- ScriptInput: https://developer.cisco.com/docs/orbital/scriptinput
- ScriptJobInfo: https://developer.cisco.com/docs/orbital/scriptjobinfo
- ScriptName: https://developer.cisco.com/docs/orbital/scriptname
- ScriptNodeResult: https://developer.cisco.com/docs/orbital/scriptnoderesult
- ScriptOutput: https://developer.cisco.com/docs/orbital/scriptoutput
- ScriptRequest: https://developer.cisco.com/docs/orbital/scriptrequest
- ScriptResponse: https://developer.cisco.com/docs/orbital/scriptresponse
- ScriptResult: https://developer.cisco.com/docs/orbital/scriptresult
- StockConfig: https://developer.cisco.com/docs/orbital/stockconfig
- String: https://developer.cisco.com/docs/orbital/string
- StringArray: https://developer.cisco.com/docs/orbital/stringarray
- SubTechniqueInfo: https://developer.cisco.com/docs/orbital/subtechniqueinfo
- SuccessOK: https://developer.cisco.com/docs/orbital/successok
- TacticInfo: https://developer.cisco.com/docs/orbital/tacticinfo
- TechniqueInfo: https://developer.cisco.com/docs/orbital/techniqueinfo
- Type: https://developer.cisco.com/docs/orbital/type
- Variants: https://developer.cisco.com/docs/orbital/variants
- VersionMatch: https://developer.cisco.com/docs/orbital/versionmatch
- Versions: https://developer.cisco.com/docs/orbital/versions
- WebhookArrayResponse: https://developer.cisco.com/docs/orbital/webhookarrayresponse
- WebhookConfig: https://developer.cisco.com/docs/orbital/webhookconfig
- WebhookJob: https://developer.cisco.com/docs/orbital/webhookjob
- WebhookJobs: https://developer.cisco.com/docs/orbital/webhookjobs
- WebhookPingResponse: https://developer.cisco.com/docs/orbital/webhookpingresponse
- WebhookPutSuccessResponseStruct: https://developer.cisco.com/docs/orbital/webhookputsuccessresponsestruct
- WebhookRequestForHandlePost: https://developer.cisco.com/docs/orbital/webhookrequestforhandlepost
- WebhookRequestForHandlePut: https://developer.cisco.com/docs/orbital/webhookrequestforhandleput
- WebhookResponseForHandlePost: https://developer.cisco.com/docs/orbital/webhookresponseforhandlepost
- WebhookResultRequest: https://developer.cisco.com/docs/orbital/webhookresultrequest
- WebhookSendResultResponse: https://developer.cisco.com/docs/orbital/webhooksendresultresponse
- WebhookSingleEntityResponseStruct: https://developer.cisco.com/docs/orbital/webhooksingleentityresponsestruct
- WebhookStatus: https://developer.cisco.com/docs/orbital/webhookstatus
- Developer Support: https://developer.cisco.com/docs/orbital/developer-support
- Glossary: https://developer.cisco.com/docs/orbital/glossary
- FAQ: https://developer.cisco.com/docs/orbital/faq

## Verified Operation Detail Example

The `Create Query` operation page exposes structured OpenAPI data. Observed operation detail:

- Operation: Create Query
- Method: `POST`
- Path: `/query`
- Security: authorization header
- Request body: JSON query model
- Successful response: job object

Project rule: when implementing against a specific API operation, open the individual operation page and verify method, path, request schema, response codes, and server region before writing code.

## Project Usage Rules

- Use this file as the Orbital API entry point for this project.
- Use the operation link index to locate the exact DevNet page for an API task.
- Do not infer request payloads from query/script examples alone; verify the API model/schema page.
- Do not store live API tokens, bearer tokens, or credentials in this workspace.
- For catalog automation, distinguish stock catalog endpoints from organization catalog endpoints.
- For script automation, distinguish catalog-script operations, live script execution, scheduled script jobs, and script job results.
- For long-running result workflows, check Results, Jobs, Downloads, Webhooks, and Remote Data Store behavior.
