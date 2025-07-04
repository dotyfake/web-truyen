<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<!-- Created by , GNU Texinfo 7.0.1 -->
  <head>
    <meta charset="utf-8">
    <title>
      Developer Documentation
    </title>
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="style.min.css">
  </head>
  <body>
    <div class="container">
      <h1>
      Developer Documentation
      </h1>


<div class="top-level-extent" id="SEC_Top">

<div class="element-contents" id="SEC_Contents">
<h2 class="contents-heading">Table of Contents</h2>

<div class="contents">

<ul class="toc-numbered-mark">
  <li><a id="toc-Introduction" href="#Introduction">1 Introduction</a></li>
  <li><a id="toc-Coding-Rules-1" href="#Coding-Rules-1">2 Coding Rules</a>
  <ul class="toc-numbered-mark">
    <li><a id="toc-Language" href="#Language">2.1 Language</a>
    <ul class="toc-numbered-mark">
      <li><a id="toc-SIMD_002fDSP-1" href="#SIMD_002fDSP-1">2.1.1 SIMD/DSP</a></li>
      <li><a id="toc-Other-languages" href="#Other-languages">2.1.2 Other languages</a></li>
    </ul></li>
    <li><a id="toc-Code-formatting-conventions" href="#Code-formatting-conventions">2.2 Code formatting conventions</a>
    <ul class="toc-numbered-mark">
      <li><a id="toc-Vim-configuration" href="#Vim-configuration">2.2.1 Vim configuration</a></li>
      <li><a id="toc-Emacs-configuration" href="#Emacs-configuration">2.2.2 Emacs configuration</a></li>
    </ul></li>
    <li><a id="toc-Comments" href="#Comments">2.3 Comments</a></li>
    <li><a id="toc-Naming-conventions-1" href="#Naming-conventions-1">2.4 Naming conventions</a></li>
    <li><a id="toc-Miscellaneous-conventions" href="#Miscellaneous-conventions">2.5 Miscellaneous conventions</a></li>
  </ul></li>
  <li><a id="toc-Development-Policy-1" href="#Development-Policy-1">3 Development Policy</a>
  <ul class="toc-numbered-mark">
    <li><a id="toc-Code-behaviour" href="#Code-behaviour">3.1 Code behaviour</a></li>
    <li><a id="toc-Patches_002fCommitting" href="#Patches_002fCommitting">3.2 Patches/Committing</a></li>
    <li><a id="toc-Code" href="#Code">3.3 Code</a></li>
    <li><a id="toc-Library-public-interfaces" href="#Library-public-interfaces">3.4 Library public interfaces</a>
    <ul class="toc-numbered-mark">
      <li><a id="toc-Adding-new-interfaces" href="#Adding-new-interfaces">3.4.1 Adding new interfaces</a></li>
      <li><a id="toc-Removing-interfaces-1" href="#Removing-interfaces-1">3.4.2 Removing interfaces</a></li>
      <li><a id="toc-Major-version-bumps-1" href="#Major-version-bumps-1">3.4.3 Major version bumps</a></li>
    </ul></li>
    <li><a id="toc-Documentation_002fOther" href="#Documentation_002fOther">3.5 Documentation/Other</a></li>
  </ul></li>
  <li><a id="toc-Submitting-patches-1" href="#Submitting-patches-1">4 Submitting patches</a></li>
  <li><a id="toc-New-codecs-or-formats-checklist" href="#New-codecs-or-formats-checklist">5 New codecs or formats checklist</a></li>
  <li><a id="toc-Patch-submission-checklist" href="#Patch-submission-checklist">6 Patch submission checklist</a></li>
  <li><a id="toc-Patch-review-process" href="#Patch-review-process">7 Patch review process</a></li>
  <li><a id="toc-Regression-tests-1" href="#Regression-tests-1">8 Regression tests</a>
  <ul class="toc-numbered-mark">
    <li><a id="toc-Adding-files-to-the-fate_002dsuite-dataset" href="#Adding-files-to-the-fate_002dsuite-dataset">8.1 Adding files to the fate-suite dataset</a></li>
    <li><a id="toc-Visualizing-Test-Coverage" href="#Visualizing-Test-Coverage">8.2 Visualizing Test Coverage</a></li>
    <li><a id="toc-Using-Valgrind" href="#Using-Valgrind">8.3 Using Valgrind</a></li>
  </ul></li>
  <li><a id="toc-Release-process-1" href="#Release-process-1">9 Release process</a>
  <ul class="toc-numbered-mark">
    <li><a id="toc-Criteria-for-Point-Releases-1" href="#Criteria-for-Point-Releases-1">9.1 Criteria for Point Releases</a></li>
    <li><a id="toc-Release-Checklist" href="#Release-Checklist">9.2 Release Checklist</a></li>
  </ul></li>
</ul>
</div>
</div>

<ul class="mini-toc">
<li><a href="#Introduction" accesskey="1">Introduction</a></li>
<li><a href="#Coding-Rules-1" accesskey="2">Coding Rules</a></li>
<li><a href="#Development-Policy-1" accesskey="3">Development Policy</a></li>
<li><a href="#Submitting-patches-1" accesskey="4">Submitting patches</a></li>
<li><a href="#New-codecs-or-formats-checklist" accesskey="5">New codecs or formats checklist</a></li>
<li><a href="#Patch-submission-checklist" accesskey="6">Patch submission checklist</a></li>
<li><a href="#Patch-review-process" accesskey="7">Patch review process</a></li>
<li><a href="#Regression-tests-1" accesskey="8">Regression tests</a></li>
<li><a href="#Release-process-1" accesskey="9">Release process</a></li>
</ul>
<div class="chapter-level-extent" id="Introduction">
<h2 class="chapter">1 Introduction</h2>

<p>This text is concerned with the development <em class="emph">of</em> FFmpeg itself. Information
on using the FFmpeg libraries in other programs can be found elsewhere, e.g. in:
</p><ul class="itemize mark-bullet">
<li>the installed header files
</li><li><a class="url" href="http://ffmpeg.org/doxygen/trunk/index.html">the Doxygen documentation</a>
generated from the headers
</li><li>the examples under <samp class="file">doc/examples</samp>
</li></ul>

<p>For more detailed legal information about the use of FFmpeg in
external programs read the <samp class="file">LICENSE</samp> file in the source tree and
consult <a class="url" href="https://ffmpeg.org/legal.html">https://ffmpeg.org/legal.html</a>.
</p>
<p>If you modify FFmpeg code for your own use case, you are highly encouraged to
<em class="emph">submit your changes back to us</em>, using this document as a guide. There are
both pragmatic and ideological reasons to do so:
</p><ul class="itemize mark-bullet">
<li>Maintaining external changes to keep up with upstream development is
time-consuming and error-prone. With your code in the main tree, it will be
maintained by FFmpeg developers.
</li><li>FFmpeg developers include leading experts in the field who can find bugs or
design flaws in your code.
</li><li>By supporting the project you find useful you ensure it continues to be
maintained and developed.
</li></ul>

<p>All proposed code changes should be submitted for review to
<a class="url" href="mailto:ffmpeg-devel@ffmpeg.org">the development mailing list</a>, as
described in more detail in the <a class="ref" href="#Submitting-patches">Submitting patches</a> chapter. The code
should comply with the <a class="ref" href="#Development-Policy">Development Policy</a> and follow the <a class="ref" href="#Coding-Rules">Coding Rules</a>.
The developer making the commit and the author are responsible for their changes
and should try to fix issues their commit causes.
</p>
<a class="anchor" id="Coding-Rules"></a></div>
<div class="chapter-level-extent" id="Coding-Rules-1">
<h2 class="chapter">2 Coding Rules</h2>

<ul class="mini-toc">
<li><a href="#Language" accesskey="1">Language</a></li>
<li><a href="#Code-formatting-conventions" accesskey="2">Code formatting conventions</a></li>
<li><a href="#Comments" accesskey="3">Comments</a></li>
<li><a href="#Naming-conventions-1" accesskey="4">Naming conventions</a></li>
<li><a href="#Miscellaneous-conventions" accesskey="5">Miscellaneous conventions</a></li>
</ul>
<div class="section-level-extent" id="Language">
<h3 class="section">2.1 Language</h3>

<p>FFmpeg is mainly programmed in the ISO C99 language, extended with:
</p><ul class="itemize mark-bullet">
<li>Atomic operations from C11 <samp class="file">stdatomic.h</samp>. They are emulated on
architectures/compilers that do not support them, so all FFmpeg-internal code
may use atomics without any extra checks. However, <samp class="file">stdatomic.h</samp> must not
be included in public headers, so they stay C99-compatible.
</li></ul>

<p>Compiler-specific extensions may be used with good reason, but must not be
depended on, i.e. the code must still compile and work with compilers lacking
the extension.
</p>
<p>The following C99 features must not be used anywhere in the codebase:
</p><ul class="itemize mark-bullet">
<li>variable-length arrays;

</li><li>complex numbers;

</li><li>mixed statements and declarations.
</li></ul>

<ul class="mini-toc">
<li><a href="#SIMD_002fDSP-1" accesskey="1">SIMD/DSP</a></li>
<li><a href="#Other-languages" accesskey="2">Other languages</a></li>
</ul>
<div class="subsection-level-extent" id="SIMD_002fDSP-1">
<h4 class="subsection">2.1.1 SIMD/DSP</h4>
<a class="anchor" id="SIMD_002fDSP"></a>
<p>As modern compilers are unable to generate efficient SIMD or other
performance-critical DSP code from plain C, handwritten assembly is used.
Usually such code is isolated in a separate function. Then the standard approach
is writing multiple versions of this function – a plain C one that works
everywhere and may also be useful for debugging, and potentially multiple
architecture-specific optimized implementations. Initialization code then
chooses the best available version at runtime and loads it into a function
pointer; the function in question is then always called through this pointer.
</p>
<p>The specific syntax used for writing assembly is:
</p><ul class="itemize mark-bullet">
<li>NASM on x86;

</li><li>GAS on ARM.
</li></ul>

<p>A unit testing framework for assembly called <code class="code">checkasm</code> lives under
<samp class="file">tests/checkasm</samp>. All new assembly should come with <code class="code">checkasm</code> tests;
adding tests for existing assembly that lacks them is also strongly encouraged.
</p>
</div>
<div class="subsection-level-extent" id="Other-languages">
<h4 class="subsection">2.1.2 Other languages</h4>

<p>Other languages than C may be used in special cases:
</p><ul class="itemize mark-bullet">
<li>Compiler intrinsics or inline assembly when the code in question cannot be
written in the standard way described in the <a class="ref" href="#SIMD_002fDSP">SIMD/DSP</a> section. This
typically applies to code that needs to be inlined.

</li><li>Objective-C where required for interacting with macOS-specific interfaces.
</li></ul>

</div>
</div>
<div class="section-level-extent" id="Code-formatting-conventions">
<h3 class="section">2.2 Code formatting conventions</h3>

<p>There are the following guidelines regarding the indentation in files:
</p>
<ul class="itemize mark-bullet">
<li>Indent size is 4.

</li><li>The TAB character is forbidden outside of Makefiles as is any
form of trailing whitespace. Commits containing either will be
rejected by the git repository.

</li><li>You should try to limit your code lines to 80 characters; however, do so if
and only if this improves readability.

</li><li>K&amp;R coding style is used.
</li></ul>
<p>The presentation is one inspired by &rsquo;indent -i4 -kr -nut&rsquo;.
</p>
<ul class="mini-toc">
<li><a href="#Vim-configuration" accesskey="1">Vim configuration</a></li>
<li><a href="#Emacs-configuration" accesskey="2">Emacs configuration</a></li>
</ul>
<div class="subsection-level-extent" id="Vim-configuration">
<h4 class="subsection">2.2.1 Vim configuration</h4>
<p>In order to configure Vim to follow FFmpeg formatting conventions, paste
the following snippet into your <samp class="file">.vimrc</samp>:
</p><div class="example">
<pre class="example-preformatted">&quot; indentation rules for FFmpeg: 4 spaces, no tabs
set expandtab
set shiftwidth=4
set softtabstop=4
set cindent
set cinoptions=(0
&quot; Allow tabs in Makefiles.
autocmd FileType make,automake set noexpandtab shiftwidth=8 softtabstop=8
&quot; Trailing whitespace and tabs are forbidden, so highlight them.
highlight ForbiddenWhitespace ctermbg=red guibg=red
match ForbiddenWhitespace /\s\+$\|\t/
&quot; Do not highlight spaces at the end of line while typing on that line.
autocmd InsertEnter * match ForbiddenWhitespace /\t\|\s\+\%#\@&lt;!$/
</pre></div>

</div>
<div class="subsection-level-extent" id="Emacs-configuration">
<h4 class="subsection">2.2.2 Emacs configuration</h4>
<p>For Emacs, add these roughly equivalent lines to your <samp class="file">.emacs.d/init.el</samp>:
</p><div class="example lisp">
<pre class="lisp-preformatted">(c-add-style &quot;ffmpeg&quot;
             '(&quot;k&amp;r&quot;
               (c-basic-offset . 4)
               (indent-tabs-mode . nil)
               (show-trailing-whitespace . t)
               (c-offsets-alist
                (statement-cont . (c-lineup-assignments +)))
               )
             )
(setq c-default-style &quot;ffmpeg&quot;)
</pre></div>

</div>
</div>
<div class="section-level-extent" id="Comments">
<h3 class="section">2.3 Comments</h3>
<p>Use the JavaDoc/Doxygen  format (see examples below) so that code documentation
can be generated automatically. All nontrivial functions should have a comment
above them explaining what the function does, even if it is just one sentence.
All structures and their member variables should be documented, too.
</p>
<p>Avoid Qt-style and similar Doxygen syntax with <code class="code">!</code> in it, i.e. replace
<code class="code">//!</code> with <code class="code">///</code> and similar.  Also @ syntax should be employed
for markup commands, i.e. use <code class="code">@param</code> and not <code class="code">\param</code>.
</p>
<div class="example">
<pre class="example-preformatted">/**
 * @file
 * MPEG codec.
 * @author ...
 */

/**
 * Summary sentence.
 * more text ...
 * ...
 */
typedef struct Foobar {
    int var1; /**&lt; var1 description */
    int var2; ///&lt; var2 description
    /** var3 description */
    int var3;
} Foobar;

/**
 * Summary sentence.
 * more text ...
 * ...
 * @param my_parameter description of my_parameter
 * @return return value description
 */
int myfunc(int my_parameter)
...
</pre></div>

<a class="anchor" id="Naming-conventions"></a></div>
<div class="section-level-extent" id="Naming-conventions-1">
<h3 class="section">2.4 Naming conventions</h3>

<p>Names of functions, variables, and struct members must be lowercase, using
underscores (_) to separate words. For example, &lsquo;<samp class="samp">avfilter_get_video_buffer</samp>&rsquo;
is an acceptable function name and &lsquo;<samp class="samp">AVFilterGetVideo</samp>&rsquo; is not.
</p>
<p>Struct, union, enum, and typedeffed type names must use CamelCase. All structs
and unions should be typedeffed to the same name as the struct/union tag, e.g.
<code class="code">typedef struct AVFoo { ... } AVFoo;</code>. Enums are typically not
typedeffed.
</p>
<p>Enumeration constants and macros must be UPPERCASE, except for macros
masquerading as functions, which should use the function naming convention.
</p>
<p>All identifiers in the libraries should be namespaced as follows:
</p><ul class="itemize mark-bullet">
<li>No namespacing for identifiers with file and lower scope (e.g. local variables,
static functions), and struct and union members,

</li><li>The <code class="code">ff_</code> prefix must be used for variables and functions visible outside
of file scope, but only used internally within a single library, e.g.
&lsquo;<samp class="samp">ff_w64_demuxer</samp>&rsquo;. This prevents name collisions when FFmpeg is statically
linked.

</li><li>For variables and functions visible outside of file scope, used internally
across multiple libraries, use <code class="code">avpriv_</code> as prefix, for example,
&lsquo;<samp class="samp">avpriv_report_missing_feature</samp>&rsquo;.

</li><li>All other internal identifiers, like private type or macro names, should be
namespaced only to avoid possible internal conflicts. E.g. <code class="code">H264_NAL_SPS</code>
vs. <code class="code">HEVC_NAL_SPS</code>.

</li><li>Each library has its own prefix for public symbols, in addition to the
commonly used <code class="code">av_</code> (<code class="code">avformat_</code> for libavformat,
<code class="code">avcodec_</code> for libavcodec, <code class="code">swr_</code> for libswresample, etc).
Check the existing code and choose names accordingly.

</li><li>Other public identifiers (struct, union, enum, macro, type names) must use their
library&rsquo;s public prefix (<code class="code">AV</code>, <code class="code">Sws</code>, or <code class="code">Swr</code>).
</li></ul>

<p>Furthermore, name space reserved for the system should not be invaded.
Identifiers ending in <code class="code">_t</code> are reserved by
<a class="url" href="http://pubs.opengroup.org/onlinepubs/007904975/functions/xsh_chap02_02.html#tag_02_02_02">POSIX</a>.
Also avoid names starting with <code class="code">__</code> or <code class="code">_</code> followed by an uppercase
letter as they are reserved by the C standard. Names starting with <code class="code">_</code>
are reserved at the file level and may not be used for externally visible
symbols. If in doubt, just avoid names starting with <code class="code">_</code> altogether.
</p>
</div>
<div class="section-level-extent" id="Miscellaneous-conventions">
<h3 class="section">2.5 Miscellaneous conventions</h3>

<ul class="itemize mark-bullet">
<li>Casts should be used only when necessary. Unneeded parentheses
should also be avoided if they don&rsquo;t make the code easier to understand.
</li></ul>

<a class="anchor" id="Development-Policy"></a></div>
</div>
<div class="chapter-level-extent" id="Development-Policy-1">
<h2 class="chapter">3 Development Policy</h2>

<ul class="mini-toc">
<li><a href="#Code-behaviour" accesskey="1">Code behaviour</a></li>
<li><a href="#Patches_002fCommitting" accesskey="2">Patches/Committing</a></li>
<li><a href="#Code" accesskey="3">Code</a></li>
<li><a href="#Library-public-interfaces" accesskey="4">Library public interfaces</a></li>
<li><a href="#Documentation_002fOther" accesskey="5">Documentation/Other</a></li>
</ul>
<div class="section-level-extent" id="Code-behaviour">
<h3 class="section">3.1 Code behaviour</h3>

<h4 class="subheading" id="Correctness">Correctness</h4>
<p>The code must be valid. It must not crash, abort, access invalid pointers, leak
memory, cause data races or signed integer overflow, or otherwise cause
undefined behaviour. Error codes should be checked and, when applicable,
forwarded to the caller.
</p>
<h4 class="subheading" id="Thread_002d-and-library_002dsafety">Thread- and library-safety</h4>
<p>Our libraries may be called by multiple independent callers in the same process.
These calls may happen from any number of threads and the different call sites
may not be aware of each other - e.g. a user program may be calling our
libraries directly, and use one or more libraries that also call our libraries.
The code must behave correctly under such conditions.
</p>
<h4 class="subheading" id="Robustness">Robustness</h4>
<p>The code must treat as untrusted any bytestream received from a caller or read
from a file, network, etc. It must not misbehave when arbitrary data is sent to
it - typically it should print an error message and return
<code class="code">AVERROR_INVALIDDATA</code> on encountering invalid input data.
</p>
<h4 class="subheading" id="Memory-allocation">Memory allocation</h4>
<p>The code must use the <code class="code">av_malloc()</code> family of functions from
<samp class="file">libavutil/mem.h</samp> to perform all memory allocation, except in special cases
(e.g. when interacting with an external library that requires a specific
allocator to be used).
</p>
<p>All allocations should be checked and <code class="code">AVERROR(ENOMEM)</code> returned on
failure. A common mistake is that error paths leak memory - make sure that does
not happen.
</p>
<h4 class="subheading" id="stdio">stdio</h4>
<p>Our libraries must not access the stdio streams stdin/stdout/stderr directly
(e.g. via <code class="code">printf()</code> family of functions), as that is not library-safe. For
logging, use <code class="code">av_log()</code>.
</p>
</div>
<div class="section-level-extent" id="Patches_002fCommitting">
<h3 class="section">3.2 Patches/Committing</h3>
<h4 class="subheading" id="Licenses-for-patches-must-be-compatible-with-FFmpeg_002e">Licenses for patches must be compatible with FFmpeg.</h4>
<p>Contributions should be licensed under the
<a class="uref" href="http://www.gnu.org/licenses/lgpl-2.1.html">LGPL 2.1</a>,
including an &quot;or any later version&quot; clause, or, if you prefer
a gift-style license, the
<a class="uref" href="http://opensource.org/licenses/isc-license.txt">ISC</a> or
<a class="uref" href="http://mit-license.org/">MIT</a> license.
<a class="uref" href="http://www.gnu.org/licenses/gpl-2.0.html">GPL 2</a> including
an &quot;or any later version&quot; clause is also acceptable, but LGPL is
preferred.
If you add a new file, give it a proper license header. Do not copy and
paste it from a random place, use an existing file as template.
</p>
<h4 class="subheading" id="You-must-not-commit-code-which-breaks-FFmpeg_0021">You must not commit code which breaks FFmpeg!</h4>
<p>This means unfinished code which is enabled and breaks compilation,
or compiles but does not work/breaks the regression tests. Code which
is unfinished but disabled may be permitted under-circumstances, like
missing samples or an implementation with a small subset of features.
Always check the mailing list for any reviewers with issues and test
FATE before you push.
</p>
<h4 class="subheading" id="Commit-messages">Commit messages</h4>
<p>Commit messages are highly important tools for informing other developers on
what a given change does and why. Every commit must always have a properly
filled out commit message with the following format:
</p><div class="example">
<pre class="example-preformatted">area changed: short 1 line description

details describing what and why and giving references.
</pre></div>

<p>If the commit addresses a known bug on our bug tracker or other external issue
(e.g. CVE), the commit message should include the relevant bug ID(s) or other
external identifiers. Note that this should be done in addition to a proper
explanation and not instead of it. Comments such as &quot;fixed!&quot; or &quot;Changed it.&quot;
are not acceptable.
</p>
<p>When applying patches that have been discussed at length on the mailing list,
reference the thread in the commit message.
</p>
<h4 class="subheading" id="Testing-must-be-adequate-but-not-excessive_002e">Testing must be adequate but not excessive.</h4>
<p>If it works for you, others, and passes FATE then it should be OK to commit
it, provided it fits the other committing criteria. You should not worry about
over-testing things. If your code has problems (portability, triggers
compiler bugs, unusual environment etc) they will be reported and eventually
fixed.
</p>
<h4 class="subheading" id="Do-not-commit-unrelated-changes-together_002e">Do not commit unrelated changes together.</h4>
<p>They should be split them into self-contained pieces. Also do not forget
that if part B depends on part A, but A does not depend on B, then A can
and should be committed first and separate from B. Keeping changes well
split into self-contained parts makes reviewing and understanding them on
the commit log mailing list easier. This also helps in case of debugging
later on.
Also if you have doubts about splitting or not splitting, do not hesitate to
ask/discuss it on the developer mailing list.
</p>
<h4 class="subheading" id="Cosmetic-changes-should-be-kept-in-separate-patches_002e">Cosmetic changes should be kept in separate patches.</h4>
<p>We refuse source indentation and other cosmetic changes if they are mixed
with functional changes, such commits will be rejected and removed. Every
developer has his own indentation style, you should not change it. Of course
if you (re)write something, you can use your own style, even though we would
prefer if the indentation throughout FFmpeg was consistent (Many projects
force a given indentation style - we do not.). If you really need to make
indentation changes (try to avoid this), separate them strictly from real
changes.
</p>
<p>NOTE: If you had to put if(){ .. } over a large (&gt; 5 lines) chunk of code,
then either do NOT change the indentation of the inner part within (do not
move it to the right)! or do so in a separate commit
</p>
<h4 class="subheading" id="Credit-the-author-of-the-patch_002e">Credit the author of the patch.</h4>
<p>Make sure the author of the commit is set correctly. (see git commit &ndash;author)
If you apply a patch, send an
answer to ffmpeg-devel (or wherever you got the patch from) saying that
you applied the patch.
</p>
<h4 class="subheading" id="Always-wait-long-enough-before-pushing-changes">Always wait long enough before pushing changes</h4>
<p>Do NOT commit to code actively maintained by others without permission.
Send a patch to ffmpeg-devel. If no one answers within a reasonable
time-frame (12h for build failures and security fixes, 3 days small changes,
1 week for big patches) then commit your patch if you think it is OK.
Also note, the maintainer can simply ask for more time to review!
</p>
</div>
<div class="section-level-extent" id="Code">
<h3 class="section">3.3 Code</h3>
<h4 class="subheading" id="Warnings-for-correct-code-may-be-disabled-if-there-is-no-other-option_002e">Warnings for correct code may be disabled if there is no other option.</h4>
<p>Compiler warnings indicate potential bugs or code with bad style. If a type of
warning always points to correct and clean code, that warning should
be disabled, not the code changed.
Thus the remaining warnings can either be bugs or correct code.
If it is a bug, the bug has to be fixed. If it is not, the code should
be changed to not generate a warning unless that causes a slowdown
or obfuscates the code.
</p>
</div>
<div class="section-level-extent" id="Library-public-interfaces">
<h3 class="section">3.4 Library public interfaces</h3>
<p>Every library in FFmpeg provides a set of public APIs in its installed headers,
which are those listed in the variable <code class="code">HEADERS</code> in that library&rsquo;s
<samp class="file">Makefile</samp>. All identifiers defined in those headers (except for those
explicitly documented otherwise), and corresponding symbols exported from
compiled shared or static libraries are considered public interfaces and must
comply with the API and ABI compatibility rules described in this section.
</p>
<p>Public APIs must be backward compatible within a given major version. I.e. any
valid user code that compiles and works with a given library version must still
compile and work with any later version, as long as the major version number is
unchanged. &quot;Valid user code&quot; here means code that is calling our APIs in a
documented and/or intended manner and is not relying on any undefined behavior.
Incrementing the major version may break backward compatibility, but only to the
extent described in <a class="ref" href="#Major-version-bumps">Major version bumps</a>.
</p>
<p>We also guarantee backward ABI compatibility for shared and static libraries.
I.e. it should be possible to replace a shared or static build of our library
with a build of any later version (re-linking the user binary in the static
case) without breaking any valid user binaries, as long as the major version
number remains unchanged.
</p>
<ul class="mini-toc">
<li><a href="#Adding-new-interfaces" accesskey="1">Adding new interfaces</a></li>
<li><a href="#Removing-interfaces-1" accesskey="2">Removing interfaces</a></li>
<li><a href="#Major-version-bumps-1" accesskey="3">Major version bumps</a></li>
</ul>
<div class="subsection-level-extent" id="Adding-new-interfaces">
<h4 class="subsection">3.4.1 Adding new interfaces</h4>
<p>Any new public identifiers in installed headers are considered new API - this
includes new functions, structs, macros, enum values, typedefs, new fields in
existing structs, new installed headers, etc. Consider the following
guidelines when adding new APIs.
</p>
<h4 class="subsubheading" id="Motivation">Motivation</h4>
<p>While new APIs can be added relatively easily, changing or removing them is much
harder due to abovementioned compatibility requirements. You should then
consider carefully whether the functionality you are adding really needs to be
exposed to our callers as new public API.
</p>
<p>Your new API should have at least one well-established use case outside of the
library that cannot be easily achieved with existing APIs. Every library in
FFmpeg also has a defined scope - your new API must fit within it.
</p>
<h4 class="subsubheading" id="Replacing-existing-APIs">Replacing existing APIs</h4>
<p>If your new API is replacing an existing one, it should be strictly superior to
it, so that the advantages of using the new API outweight the cost to the
callers of changing their code. After adding the new API you should then
deprecate the old one and schedule it for removal, as described in
<a class="ref" href="#Removing-interfaces">Removing interfaces</a>.
</p>
<p>If you deem an existing API deficient and want to fix it, the preferred approach
in most cases is to add a differently-named replacement and deprecate the
existing API rather than modify it. It is important to make the changes visible
to our callers (e.g. through compile- or run-time deprecation warnings) and make
it clear how to transition to the new API (e.g. in the Doxygen documentation or
on the wiki).
</p>
<h4 class="subsubheading" id="API-design">API design</h4>
<p>The FFmpeg libraries are used by a variety of callers to perform a wide range of
multimedia-related processing tasks. You should therefore - within reason - try
to design your new API for the broadest feasible set of use cases and avoid
unnecessarily limiting it to a specific type of callers (e.g. just media
playback or just transcoding).
</p>
<h4 class="subsubheading" id="Consistency">Consistency</h4>
<p>Check whether similar APIs already exist in FFmpeg. If they do, try to model
your new addition on them to achieve better overall consistency.
</p>
<p>The naming of your new identifiers should follow the <a class="ref" href="#Naming-conventions">Naming conventions</a>
and be aligned with other similar APIs, if applicable.
</p>
<h4 class="subsubheading" id="Extensibility">Extensibility</h4>
<p>You should also consider how your API might be extended in the future in a
backward-compatible way. If you are adding a new struct <code class="code">AVFoo</code>, the
standard approach is requiring the caller to always allocate it through a
constructor function, typically named <code class="code">av_foo_alloc()</code>. This way new fields
may be added to the end of the struct without breaking ABI compatibility.
Typically you will also want a destructor - <code class="code">av_foo_free(AVFoo**)</code> that
frees the indirectly supplied object (and its contents, if applicable) and
writes <code class="code">NULL</code> to the supplied pointer, thus eliminating the potential
dangling pointer in the caller&rsquo;s memory.
</p>
<p>If you are adding new functions, consider whether it might be desirable to tweak
their behavior in the future - you may want to add a flags argument, even though
it would be unused initially.
</p>
<h4 class="subsubheading" id="Documentation">Documentation</h4>
<p>All new APIs must be documented as Doxygen-formatted comments above the
identifiers you add to the public headers. You should also briefly mention the
change in <samp class="file">doc/APIchanges</samp>.
</p>
<h4 class="subsubheading" id="Bump-the-version">Bump the version</h4>
<p>Backward-incompatible API or ABI changes require incrementing (bumping) the
major version number, as described in <a class="ref" href="#Major-version-bumps">Major version bumps</a>. Major
bumps are significant events that happen on a schedule - so if your change
strictly requires one you should add it under <code class="code">#if</code> preprocesor guards that
disable it until the next major bump happens.
</p>
<p>New APIs that can be added without breaking API or ABI compatibility require
bumping the minor version number.
</p>
<p>Incrementing the third (micro) version component means a noteworthy binary
compatible change (e.g. encoder bug fix that matters for the decoder). The third
component always starts at 100 to distinguish FFmpeg from Libav.
</p>
<a class="anchor" id="Removing-interfaces"></a></div>
<div class="subsection-level-extent" id="Removing-interfaces-1">
<h4 class="subsection">3.4.2 Removing interfaces</h4>
<p>Due to abovementioned compatibility guarantees, removing APIs is an involved
process that should only be undertaken with good reason. Typically a deficient,
restrictive, or otherwise inadequate API is replaced by a superior one, though
it does at times happen that we remove an API without any replacement (e.g. when
the feature it provides is deemed not worth the maintenance effort, out of scope
of the project, fundamentally flawed, etc.).
</p>
<p>The removal has two steps - first the API is deprecated and scheduled for
removal, but remains present and functional. The second step is actually
removing the API - this is described in <a class="ref" href="#Major-version-bumps">Major version bumps</a>.
</p>
<p>To deprecate an API you should signal to our users that they should stop using
it. E.g. if you intend to remove struct members or functions, you should mark
them with <code class="code">attribute_deprecated</code>. When this cannot be done, it may be
possible to detect the use of the deprecated API at runtime and print a warning
(though take care not to print it too often). You should also document the
deprecation (and the replacement, if applicable) in the relevant Doxygen
documentation block.
</p>
<p>Finally, you should define a deprecation guard along the lines of
<code class="code">#define FF_API_&lt;FOO&gt; (LIBAVBAR_VERSION_MAJOR &lt; XX)</code> (where XX is the major
version in which the API will be removed) in <samp class="file">libavbar/version_major.h</samp>
(<samp class="file">version.h</samp> in case of <code class="code">libavutil</code>). Then wrap all uses of the
deprecated API in <code class="code">#if FF_API_&lt;FOO&gt; .... #endif</code>, so that the code will
automatically get disabled once the major version reaches XX. You can also use
<code class="code">FF_DISABLE_DEPRECATION_WARNINGS</code> and <code class="code">FF_ENABLE_DEPRECATION_WARNINGS</code>
to suppress compiler deprecation warnings inside these guards. You should test
that the code compiles and works with the guard macro evaluating to both true
and false.
</p>
<a class="anchor" id="Major-version-bumps"></a></div>
<div class="subsection-level-extent" id="Major-version-bumps-1">
<h4 class="subsection">3.4.3 Major version bumps</h4>
<p>A major version bump signifies an API and/or ABI compatibility break. To reduce
the negative effects on our callers, who are required to adapt their code,
backward-incompatible changes during a major bump should be limited to:
</p><ul class="itemize mark-bullet">
<li>Removing previo