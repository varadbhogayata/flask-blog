-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 29, 2020 at 04:35 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.2.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `blogdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `sno` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(100) NOT NULL,
  `mob_num` varchar(14) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sno`, `name`, `email`, `mob_num`, `msg`, `date`) VALUES
(1, 'first post', 'firstpost@gmail.com', '123456789', 'FIRST POST', '2020-05-27 16:30:06'),
(2, 'john doe', 'johndoe@gmail.com', '4545451212', 'Hi', '2020-05-27 16:30:25');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `sno` int(11) NOT NULL,
  `title` text NOT NULL,
  `tagline` text NOT NULL,
  `slug` varchar(30) NOT NULL,
  `content` text NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp(),
  `img_file` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `title`, `tagline`, `slug`, `content`, `date`, `img_file`) VALUES
(1, 'First Post updated', 'first tagline updated', 'first-post', 'This is my first blog. It is made using flask micro framework. UPDATED', '2020-05-28 20:08:49', 'not-found.pn'),
(2, 'This is the second post.', 'second tagline', 'second-post', 'This tutorial will walk you through creating a basic blog application called Flaskr. Users will be able to register, log in, create posts, and edit or delete their own posts. You will be able to package and install the application on other computers.It’s assumed that you’re already familiar with Python. The official tutorial in the Python docs is a great way to learn or review first.\r\n\r\nWhile it’s designed to give a good starting point, the tutorial doesn’t cover all of Flask’s features. Check out the Quickstart for an overview of what Flask can do, then dive into the docs to find out more. The tutorial only uses what’s provided by Flask and Python. In another project, you might decide to use Extensions or other libraries to make some tasks simpler.\r\n\r\n', '2020-05-28 17:04:50', 'about-bg.jpg'),
(3, 'flask tutorial', 'learn flask in 10 minutes', 'third-post', 'Flask is flexible. It doesn’t require you to use any particular project or code layout. However, when first starting, it’s helpful to use a more structured approach. This means that the tutorial will require a bit of boilerplate up front, but it’s done to avoid many common pitfalls that new developers encounter, and it creates a project that’s easy to expand on. Once you become more comfortable with Flask, you can step out of this structure and take full advantage of Flask’s flexibility.\r\n\r\n', '2020-05-28 17:12:18', 'about-bg.jpg'),
(5, 'Fifth Post - Learn templates', 'Are bhai bhai! You have reached to 5th post.', 'fifth-post', 'You’ve written the authentication views for your application, but if you’re running the server and try to go to any of the URLs, you’ll see a TemplateNotFound error. That’s because the views are calling render_template(), but you haven’t written the templates yet. The template files will be stored in the templates directory inside the flaskr package.\r\n\r\nTemplates are files that contain static data as well as placeholders for dynamic data. A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates.\r\n\r\nIn your application, you will use templates to render HTML which will display in the user’s browser. In Flask, Jinja is configured to autoescape any data that is rendered in HTML templates. This means that it’s safe to render user input; any characters they’ve entered that could mess with the HTML, such as < and > will be escaped with safe values that look the same in the browser but don’t cause unwanted effects.\r\n\r\nJinja looks and behaves mostly like Python. Special delimiters are used to distinguish Jinja syntax from the static data in the template. Anything between {{ and }} is an expression that will be output to the final document. {% and %} denotes a control flow statement like if and for. Unlike Python, blocks are denoted by start and end tags rather than indentation since static text within a block could change indentation.\r\n\r\n', '2020-05-28 17:14:31', 'about-bg.jpg'),
(6, 'Sixth Post', 'Another post coming on this way!', 'sixth-post', 'Each page in the application will have the same basic layout around a different body. Instead of writing the entire HTML structure in each template, each template will extend a base template and override specific sections.\r\n\r\nflaskr/templates/base.html\r\n<!doctype html>\r\n<title>{% block title %}{% endblock %} - Flaskr</title>\r\n<link rel=\"stylesheet\" href=\"{{ url_for(\'static\', filename=\'style.css\') }}\">\r\n<nav>\r\n  <h1>Flaskr</h1>\r\n  <ul>\r\n    {% if g.user %}\r\n      <li><span>{{ g.user[\'username\'] }}</span>\r\n      <li><a href=\"{{ url_for(\'auth.logout\') }}\">Log Out</a>\r\n    {% else %}\r\n      <li><a href=\"{{ url_for(\'auth.register\') }}\">Register</a>\r\n      <li><a href=\"{{ url_for(\'auth.login\') }}\">Log In</a>\r\n    {% endif %}\r\n  </ul>\r\n</nav>\r\n<section class=\"content\">\r\n  <header>\r\n    {% block header %}{% endblock %}\r\n  </header>\r\n  {% for message in get_flashed_messages() %}\r\n    <div class=\"flash\">{{ message }}</div>\r\n  {% endfor %}\r\n  {% block content %}{% endblock %}\r\n</section>\r\ng is automatically available in templates. Based on if g.user is set (from load_logged_in_user), either the username and a log out link are displayed, or links to register and log in are displayed. url_for() is also automatically available, and is used to generate URLs to views instead of writing them out manually.\r\n\r\nAfter the page title, and before the content, the template loops over each message returned by get_flashed_messages(). You used flash() in the views to show error messages, and this is the code that will display them.\r\n\r\nThere are three blocks defined here that will be overridden in the other templates:\r\n\r\n', '2020-05-28 17:15:30', 'about-bg.jpg'),
(8, 'asdfasdf', 'sadf', 'asdf', 'asdf', '2020-05-28 19:57:16', 'sdf');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
