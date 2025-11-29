# GitHub Guide

This page is still under construction, but please add your GitHub username and actual name here:

1. Kelly - kdizzlle 
2. Javier - ~~Jamm264~~
3. Kainoah - ~~KainoahVann~~
4. Christian - ~~christiandi0r~~
5. Matthew - ~~wrong-formatt~~
6. Kevin Kopcinski - ~~BarCode32~~
7. Jacqueline Yeo - ~~Jyeo1006~~
8. Austin Duong - ~~aduong18~~
9. Ceir Prum - ~~annamuse1~~
10. Ibrahim Elsousi - ~~Medikonin~~
11. Chloe Lau - ~~cvlau~~
12. Cristian Vargas - Cristian V.
    1. couldnt find
13. Tri Do - ~~SP1RYTUSzz~~
14. Tran Vo - ~~VTMT0905~~
15. Neylton Paul Latigo - ~~Lordnimpsberry~~
16. Naomi Harford - ~~Naomibug~~
17. Lance Taningco - ~~lancetaningco~~
18. Bryton King - ~~bk225~~
19. Michael Hawkins - ~~MikeeHawkins~~
20. Kaushik Velidandla - ~~kvtrey5~~
21. Valerie Fabbri Menna - ~~valeriefm~~
22. Christopher Huizar - ~~HuizarCJ~~
23. Ben Mudgett - ~~BMudgett~~
24. Nathaniel Santella - ~~spoonprogram~~
25. Ethan Guzman -~~erguthub~~
26. Zachary Karazin - ~~Zdawg28~~
27. Harrison Chung - ~~harrisonchung06~~
28. Lukas Sandau - ~~soundcue~~
29. Giselle Revolorio- ~~Revo03~~
30. William Hsu - ~~ShadowFruits~~
31. Jordy Samaniego - ~~JSamaniego01~~
32. Jacob Showman - ~~Bear4224~~
33. Anthony Sandoval - ~~as-470~~
34. Ella Shepherd-        ~~e-shep~~
35. Audrey Ellwanger- ~~Aud-Ellwanger~~
36. Alex Martinez - ~~Alexm034~~
37. Johann Lam - johannlam-104
38. Angel Reyna -**ajreyna12**

# 🚧THE REST OF THIS PAGE IS UNDER CONSTRUCTION. IGNORE FOR NOW.🚧

# Vocabulary and Important Concepts

## Fetching, Commits, and Pull Requests

When editing files locally, it is important to make sure that your local repo is as up to date as possible before you start making changes. This will reduce the risk of conflicts later on. To do this, in GitHub Desktop we “Fetch origin”. 

Once the local repo is updated and we have made some changes, we have to make a commit. 

## Branches and Forks

https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches

In GitHub, there is a `main` branch, which is the master/default branch for repositories. You can also create your own custom branch of the main branch, where you can do your own development without cluttering the main branch. 

This is very important for version control and working in teams. If everyone on the team was working in the same branch, we would run into `conflicts`. GitHub doesn’t play nice with group editing like Word or Google Docs. In GitHub, all changes must be checked to make sure none of the updates are fighting each other.

# How to Use GitHub

## Setup

https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository

### Using GitHub Desktop

GitHub Desktop can only be used on Windows and Mac. It is not supported on Linux.

1. Install [GitHub Desktop](https://docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop?platform=mac)
2. On the web, go to the GitHub repository you wish to clone. For this example we will be cloning the [CADENCE-docs](https://github.com/BroncoSpace-Lab/CADENCE-docs) GitHub repo.
3. Once you see the repo, click on the big green button that says `<> Code`

![image.png](image.png)

1. Click on `Open with GitHub Desktop`

![image.png](image%201.png)

1. When GitHub Desktop opens, you will see the following pop-up. Feel free to change the local path to wherever you want your GitHub repo to be stored on your computer. Then click `Clone`

![image.png](image%202.png)

1. The screen will look like this. Navigate to where it says `Current branch`

![image.png](image%203.png)

1. Select `New branch`

![image.png](image%204.png)

1. Name your branch what you want. It is generally a good idea to include your name, sub-team, or your specific task. For something like docs, your name or sub-team is fine. Here, I’ve named mine `kelly-dev`. Click `Create branch`. Make sure to `Publish branch` on the next page to make your newly created branch appear online.

![image.png](image%205.png)

1. This is what it will normally look like when you open GitHub Desktop. You can see that `CADENCE-docs` is the currently active repo in the top left corner. In the main portion of the screen, you will see a few options to navigate to the currently active repository in your computer. 
    1. You can open in Visual Studio Code (VS Code) which is usually best for editing docs and writing code.
    2. You can Show in Explorer (or equivalent file manager) do view where the files are stored locally. This is pretty much good for any use.
    3. You can also view the repo in your web browser. It’s a little annoying to edit there sometimes, so that is mainly there as a quick link to view it on the web and see the most updated version of the main branch.

![image.png](image%206.png)

1. Now you can make changes and develop in your own GitHub branch. 

### Using Terminal/Command Line

This is primarily for Linux users.

1. Open terminal and use the following commands to install git.
    
    ```powershell
    sudp apt update
    sudo apt install git
    ```
    
2. Set the global username and email to the ones associated with your GitHub account. (check your account settings online to be sure it’s the same).
    
    https://docs.github.com/en/get-started/git-basics/setting-your-username-in-git
    
    ```powershell
    git config --global user.name "your username"
    ```
    
    You can check to see if it worked with the following command. It should output your username to the terminal.
    
    ```powershell
    git config --global user.name
    ```
    
    Do the same thing with your email.
    
    https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address
    
    ```powershell
    git config --global user.email "youremail@example.com"
    ```
    
    You can check to see if it worked with the following command.
    
    ```powershell
    git config --global user.name
    ```
    

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

## Regular Use

Once you have made some changes on your branch and wish to publish them, we will do what is called a **pull request**. In this example, I have simply updated the acronym for CADENCE-SWANS in the CADENCE-docs READ.ME, but when you make a pull request there will usually be more significant changes.

### When to make a pull request

https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests

We don’t want to clutter the main branch with hundreds of pull requests for the smallest changes. We generally only do a commit and pull request when a decent amount of changes have been made, or if you have reached some sort of milestone.

It’s a balance of committing enough to reflect important changes, and waiting until you have enough changes. With a large team like this, it will be something we have to figure out together.

### In GitHub Desktop

1. Sometimes, you may have to Fetch origin to bring your updates into GitHub Desktop. Once they are there, you should see them on the screen like this:
    1. It shows what you removed in red, and what you added in green.

![image.png](image%207.png)

1. When you are ready to update your branch, write a title for the commit/pull request and a description of the changes if you want. (the title is required, the description is optional but helpful for larger updates) This is in the bottom left corner.

![image.png](image%208.png)

1. When you are done, click `Commit to (your branch)`. It may take a few seconds to process for larger commits. Once it loads, click `Push origin` to create your pull request on your branch. 

![image.png](image%209.png)

1. Once you have pushed to origin, the pull request will then be reviewed by your sub-team lead or CE/PM to be brought to the main branch. **Do not approve these yourself unless you have explicit permission.**
    1. With a large team, it is important that only a few people have the authority to merge changes to main to keep conflicts in branches to a minimum.