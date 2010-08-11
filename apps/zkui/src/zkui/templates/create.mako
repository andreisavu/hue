<%namespace name="shared" file="shared_components.mako" />

${shared.header("ZooKeeper Browser > Create Znode")}

<h2>Create New Znode</h2>
<hr /><br />

<form action="" method="POST">
  <label>Parent Path:</label>
  <input type="text" name="parent" value="${path}" />


  <button type="submit">Create</button> 
</form>

${shared.footer()}
