# App Specification

## App Name
faes-website

## Description
A static site for the Fundashon Abram Edgardo Salas

## Goals
- very simple to manage and maintain
- modern and elegant design

## Users
- Potential recipient of grants as well as the public in genera

## Key Features
### Github
- Deployed as a github pages web site
- Deployment occurs each time we do a push

### Static
- The site is not interactive. It is static html,css and js.
- All the content for the site comes from the content/ directory
- A python program will generate all the .html, css, javasrcript for a beautiful sie


## Content
- All content comes from the irectory content/
- In order to upate the site the user (Pito) edits files inside the content/ directory
- When the site is pushed to github, an action fires off to regenerate the site
- There will be subfolders in content/ eventually reflecting different types of content
- Content itself will be markdown with front matter
- There will be a distinction between private and public content. Only public content will appear on the web ite.

## Design
- We are going for a simple, modern and elegant design

## Grants
- Will have a grant type (initially "pilot" vs. "primary")
- Money is in XCG (Curacao gilders)

- 